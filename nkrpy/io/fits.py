"""Module loads/manipulates/saves its files."""

# internal modules
import os
import re

# external modules
import astropy
from astropy.io import fits as astropy__fits
import numpy as np

# relative modules
from ..misc.functions import typecheck

# global attributes
__all__ = ['read', 'write', 'make_nan', 'make_zero', 'get_resolving_power',
           'header_radec', 'create_header', 'reference', 'get_wcs_from_header']
__doc__ = """."""
__filename__ = __file__.split('/')[-1].strip('.py')
__path__ = __file__.strip('.py').strip(__filename__)


def __resolve_header(h, key: str):
    key = key.lower()
    for k in h.keys():
        if key == k.lower():
            return h[k]
    return None


def get_resolving_power(h=None, d=None):
    """d (if provided) must be 1d array of x vals"""
    if h is None and d is None:
        return
    if h is None:
        df = np.diff(d)
        rp = df / d[:-1]
        return np.median(rp)
    else:
        return __resolve_header(h, f'rp')


def get_wcs_from_header(h: dict, axis=1):
    """Create WCS array from header: dict."""
    numvals = __resolve_header(h, f'NAXIS{axis}')
    crval = __resolve_header(h, f'CRVAL{axis}')
    crval = crval if crval else 0
    crpix = __resolve_header(h, f'CRPIX{axis}')
    crpix = crpix if crpix else 0
    crdel = __resolve_header(h, f'CRDEL{axis}')
    crdel = crdel if crdel else __resolve_header(h, f'CDELT{axis}')
    crdel = crdel if crdel else __resolve_header(h, f'CD{axis}_{axis}')
    return reference(crval, crpix, crdel, numvals)


def create_header(h):
    """Creater a header.

    Take common types, recast to dict, create header.
    Required that KEY is if you input a str or Iterable(str)
    Feeding in a str is the most stable and tested method.

    h = ('KEY= VALUE', ...)
    h = {'KEY= VALUE', ...}
    h = (('KEY', 'VALUE'), ...)
    h = {KEY: VALUE, ...}
    h = 'KEY= VALUE KEY= VALUE'

    Parameters
    ----------
    h: iterable | str

    Returns
    -------
    astropy.io.fits.header.Header | None
        returns a header

    """
    CARD_MX_LEN = 22
    if isinstance(h, astropy__fits.header.Header):
        return h
    if isinstance(h, tuple) or isinstance(h, list) or isinstance(h, set):
        if typecheck(h[0]):
            h = dict(h)
        else:
            h = dict(([x.split('=') for x in h]))
    if isinstance(h, str):
        ind0 = h.index('HISTORY')
        h = [h[:ind0], h[len('history') + ind0 + 1:]]
        h[-1] = h[-1].replace('HISTORY', ' ')
        h = 'HISTORY= '.join(h)
        regex = r"([A-Z,0-9,_]*\s*=)"
        matches = re.finditer(regex, str(h), re.MULTILINE)
        for num, match in enumerate(matches, start=1):
            linestart = match.group()
            if linestart.replace(' ', '').replace('=', '') == '':
                continue
            h = h.replace(linestart, f';;;{linestart}')
        tmp = []
        for line in h.split(';;;'):
            if line.replace(' ', '').replace('=', '') == '':
                continue
            ind0 = line.index('=')
            key, value = line[:ind0], line[ind0 + 1:]
            key = key.replace(' ', '')
            value = ' / '.join([v.strip(' ').strip('"').strip("'")
                                .rjust(CARD_MX_LEN) for v in value.split('/')])
            tmp.append((key, value))
        ret = dict(tmp)
    elif isinstance(h, dict):
        ret = h
    else:
        ret = dict(h)
    #print('ret:', ret)
    return astropy__fits.header.Header(ret)


def open(fname: str):
    return read(fname)


def read(fname: str, squeeze: bool=True):
    """Read in the file and neatly close.

    Parameters
    ----------
    fname: str
        filename

    """
    header, data = [], []
    ho, do = [], []
    with astropy__fits.open(fname) as hdul:
        for h in hdul:
            header.append(h.header)
            data.append(h.data)
    if len(header) == 1:
        header, data = header[0], data[0]
        data = np.squeeze(data)
    return header, data


def write(f, fname=None, header=None, data=None, overwrite: bool = True):
    """Open and read from the file.

    If the file exists, will attempt to update either
    and or both the header and data. Otherwise creates
    the file.

    Parameters
    ----------
    f: str
        file. Can be a filename or an HDU object If it is a string,
            will set fname = f unless fname is set.
    fname: str
        filename
    header: dict
        hduheader
    data: numpy.array
        Data to write

    """
    if isinstance(f, str):
        # if string
        #print('Found string')
        if isinstance(fname, str):
            f = fname
        if os.path.isfile(f):
            # open and update
            os.system(f'rm -f {f}')
        hdu = astropy__fits.PrimaryHDU(data)
        if header is not None:
            hdr = hdu.header
            for h, v in header.items():
                if isinstance(v, str):
                    v = v.upper()
                try:
                    hdr[h.upper()] = v
                except Exception as e:
                    print(e)
                    print('Skipping header: ', h)
                    continue

        hdu.writeto(f)

    elif isinstance(f, astropy__fits.hdu.hdulist.HDUList):
        #print('Found HDUList')
        if header is not None:
            f[0].header = header
        if data is not None:
            f[0].data = data
        if fname is not None:
            f.writeto(fname)
        else:
            f.flush()
    elif isinstance(f, astropy__fits.hdu.image.PrimaryHDU):
        #print('Found PrimaryHDU')
        if header is not None:
            f.header = header
        if data is not None:
            f.data = data
        if fname is not None:
            f.writeto(fname)
        else:
            f.flush()
    return True


def make_nan(filename: str):
    """Convert a file to nan and save to nan_filename.

    Will read in the file and convert the data to nan.

    Parameters:
    -----------
    filename: str
        name of the file to convert to nans

    Returns
    -------
    None

    """
    header, data = read(filename)
    data[:] = np.nan
    write(f'nan_{filename}', header=header, data=data)


def make_zero(filename: str):
    """Convert a file to zero and save to zero_filename.

    Will read in the file and convert the data to zero.

    Parameters:
    -----------
    filename: str
        name of the file to convert to zeros

    Returns
    -------
    None

    """
    header, data = read(filename)
    data[:] = 0
    write(f'zero_{filename}', header=header, data=data)


def header_radec(header: dict):
    """Resolve a header to radec array.

    Parameters:
    -----------
    header: dict
        dictionary that holds radec conversions from fits

    Returns
    -------
    rapix: numpy.ndarray
        Array from start-end of ra the size of the fits image.
    decpix: numpy.ndarray
        Array from start-end of dec the size of the fits image.

    """
    size = (header['NAXIS1'], header['NAXIS2'])
    pix = (header['CRPIX1'], header['CRPIX2'])
    val = (header['CRVAL1'], header['CRVAL2'])
    if 'CDELT1' in header.keys():
        delta = (header['CDELT1'], header['CDELT2'])
    else:
        delta = (header['CD1_1'], header['CD2_2'])
    return map(lambda x: reference(*x), zip((val, pix, delta, size)))


def reference(crval: float, crpix: int, cdelt: float, num: int):
    """Convert typical header arguments to array.

    Parameters
    ----------
    crval: float
        The reference value at reference pix
    crpix: int
        The reference pix
    cdelt: float
        The amount crval changes per pixel positive.
    num: int
        The number of pixels.

    """
    a = np.arange(0, num, dtype=np.float)
    a *= cdelt
    a += crval - crpix
    return a

# end of code
