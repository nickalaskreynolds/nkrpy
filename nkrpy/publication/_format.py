"""Format for publication and programming."""

# internal modules
from decimal import Decimal

# external modules
import numpy as np

# relative modules
from ..misc.functions import typecheck

# global attributes
__all__ = ['scientific_format', 'decimal_format', 'general_format',
           'fortran_format', 'wrapper', 'ppi', 'formatlatex']
__doc__ = """."""
__filename__ = __file__.split('/')[-1].strip('.py')
__path__ = __file__.strip('.py').strip(__filename__)


ppi = 72



def formatlatex(value,up, lo, precision=None):
    highest_prec = f'{min([up, lo]):0.1e}' # this will be some #.####e##
    num_dec = int(highest_prec.split('e')[-1])
    if precision is not None:
        if num_dec > -precision:
            up += 10 ** (-precision)
            highest_prec = f'{min([up, lo]):0.1e}' # this will be some #.####e##
            num_dec = int(highest_prec.split('e')[-1])
    if num_dec <= 0:
        # some small number
        splits = [ ('{' + f':1.{abs(num_dec) + 1}' + 'f}').format(i) for i in [value, up, lo]]
    elif num_dec > 0:
        fac = 10 ** (num_dec)
        splits = [f'{round(i / fac, 1) * fac:n}'  for i in [value, up, lo]]
    return splits



def __resolve_format(name: str):
    funcs = globals()
    func = [globals()[f] for f in funcs if name in f]
    if len(func) == 0:
        return None
    return func[0]


def wrapper(nums, format: str = 'scientific') -> list:
    """Intelligently format data."""
    if not typecheck(nums):
        nums = [nums]
    func = __resolve_format(format)
    finder = [(len(str(num)), len(str(num).split('.')[-1])) for num in nums]
    maxlen, maxprec = zip(*finder)
    maxlen = max(maxlen)
    maxprec = min(maxprec)
    if 'sci' in format:
        nums = list(map(lambda x: func(x, maxlen), nums))
    elif 'fortran' in format:
        nums = list(map(lambda x: func(x, maxprec, maxlen), nums))
    elif 'decimal' in format:
        nums = list(map(lambda x: func(x, maxprec), nums))
    return nums


def fortran_format(num, precision: int = 3, pad: int = 10) -> str:
    """Scientific Notation formatter.

    Parameters
    ----------
    num: str
        The number (string castable) to format
    precision: int
        The precision to use
    Returns
    -------
    str:
        The formatted string

    """
    form = general_format(num, precision, pad, None, 'D')
    return form


def decimal_format(num, precision: int = 3) -> str:
    """Scientific Notation formatter.

    Parameters
    ----------
    num: str
        The number (string castable) to format
    precision: int
        The precision to use
    Returns
    -------
    str:
        The formatted string

    """
    form = general_format(num, precision, None, None, 'D')
    return form


def scientific_format(num, precision: int = 3) -> str:
    """Scientific Notation formatter.

    Parameters
    ----------
    num: str
        The number (string castable) to format
    precision: int
        The precision to use
    Returns
    -------
    str:
        The formatted string

    """
    form = general_format(num, precision, None, None, 'x10$^{')
    form = f'{form}' + '}$'
    return form


def general_format(x, precision: int = 2, pad: int = 10,
                   left: bool = False, fmt: str = 'D') -> str:
    """General formatter.

    Parameters
    ----------
    x: str
        The number (string castable) to be formatted
    precision: int
        The precision of the formatter. In sig figs
    pad: int
        The amount to pad the string to
    left_pad: bool
        If False will right pad the string,
    fmt: str
        The delimiting string between the # and the exp
    Returns
    -------
    str
        The formatted number as a string

    """
    x = str(x)
    if len(x.replace('.', '').strip('0')) < precision:
        if '.' not in x:
            x += '.' + precision * '0'
        else:
            x += precision * '0'
    x = Decimal(x)
    tup = x.as_tuple()
    digits = list(tup.digits[:precision + 1])
    sign = '-' if tup.sign else '+'
    dec = ''.join(map(str, digits[1:]))
    exp = x.adjusted()
    ret = f'{sign}{digits[0]}.{dec}{fmt}{exp}'
    if not pad:
        return ret
    if not left:
        return ret.rjust(pad)
    return ret.ljust(pad)

# end of code

# end of file
