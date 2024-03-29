"""Handle AtomicLine searching and configuration."""

# standard modules

# external modules
import numpy as np

# relative modules
from ..._types import LinesClass
from ... import Unit
from . import linelist as base_lines
from ...misc.frozendict import FrozenDict as frozendict
from ..._math._miscmath import rolling_average_value

__filename__ = __file__.split('/')[-1].strip('.py')
__path__ = __file__.strip('.py').strip(__filename__)
__all__ = ['Lines',]


class Lines(LinesClass):
    """ Define and extract common atomic Lines

    Houses all useful atomic lines and short program for parsing.

    The overview of how this module operates on the backend,
     * User defines a band (NIR, etc), a unit (meters, Hz, etc),
        and possibly limits.
     * The program will try to resolve the band to the known bands
        and the unit to the known units.
     * Then it will populate a preliminary configuration dict
     * Then this dict is fed into the nkrpy.unit resolver and
        this is saved to a new dict
     * If regions were specified, then they are regenerated.

    Parameters
    ----------
    band: str
        common band to extract. Default 'nir'
    unit: str
        common unit to convert lines to
    xlower: float
        The lower limit to extract in units specified as unit
    xupper: float
        The upper limit to extract units specified as unit
    aperture: float
        The spacing to greedily consume lines by
    remove_lines: list
        This is very particular. But removes these lines from the output line list. Names must match exactly
    allowed_lines: list
        Similary this allows lines. This overrides remove lines if specified. Names must match exactly.

    Methods
    -------
    add_lines
    aperture
    is_line
    refresh
    remove_lines
    remove_region
    reset
    resolve_band
    return_config
    return_labels
    return_lines
    return_types
    iterate_base_atomiclines

    """
    __types = base_lines.keys()
    __base_atomiclines = frozendict(**base_lines)

    def __new__(cls, *args, **kwargs):
        """Dunder."""
        cls.__base_config = frozendict(**{'band': 'nir', 'unit': 'meters',
                                          'xlower': -1, 'xupper': -1,
                                          'aperture': None,
                                          'remove_lines': set(),
                                          'allowed_lines': set()})
        return super(Lines, cls).__new__(cls)

    def setup(self, band: str = 'nir', unit: str = 'meters',
                 xlower: float = -1, xupper: float = -1,
                 aperture: float = None, remove_lines: list = None,
                 allowed_lines: list = None):
        self.__reset()
        self.__config['band'] = self.resolve_band(band)
        self.__config['unit'] = Unit.resolve_unit(unit)['name']
        if remove_lines is None:
            remove_lines = []
        if allowed_lines is None:
            allowed_lines = []
        if remove_lines == ['all']:
            remove_lines = set(self.__base_atomiclines.keys())
        if allowed_lines == ['all']:
            allowed_lines = set(self.__base_atomiclines.keys())
        self.__config.update({'xlower': xlower,
                              'xupper': xupper,
                              'aperture': aperture,
                              'remove_lines': set(remove_lines),
                              'allowed_lines': set(allowed_lines)})
        self.__populate_lines()
        self.__refresh()


    def __init__(self, *args, **kwargs):
        """Initilization Magic Method."""
        self.setup(*args, **kwargs)

    def __reset(self):
        """Reset the class attributes."""
        self.__lines = {}
        self.__config = dict(self.__base_config)
        self.__base_atomiclines = frozendict(**self.__base_atomiclines[self.__config['band']])  # noqa
        self.__populate_lines()

    def __populate_lines(self):
        for linename, lineinfo in self.__base_atomiclines.items():
            if (linename in self.__config['remove_lines']) and\
               (linename not in self.__config['allowed_lines']):
                continue
            vals = Unit(baseunit=lineinfo['unit'],
                        convunit=self.__config['unit'],
                        vals=lineinfo['val'], sort=True)
            self.__lines[linename] = {
                'baseunit': lineinfo['unit'],
                'convunit': self.__config['unit'],
                'vals': vals.get_vals(),
                'rank': lineinfo['rank'],
            }

    def __compute_aperture(self, line_agnostic: bool=False):
        ap = self.__config['aperture']
        if ap is None or ap <= 0:
            self.__populate_lines()
            return
        if line_agnostic:
            _ap = []
            keylist = {}
            for i, key in enumerate(self.__lines.keys()):
                if key not in keylist:
                    keylist[key] = i
                vals = self.__lines[key]['vals']
                self.__lines[key]['vals'] = []
                _ap.extend(list(zip(np.array(vals), len(vals) * [i])))

            _ap = (rolling_average_value(np.array(_ap), ap)).tolist()

            for i, row in enumerate(_ap):
                row = [[abs(row[-1] - val), key] for key, val in keylist.items()]
                row.sort(key=lambda x: x[0])
                row = row[0]
                key = row[-1]
                self.__lines[key]['vals'].append(row[0])
        else:
            for i, key in enumerate(self.__lines.keys()):
                vals = self.__lines[key]['vals']
                _ap = (rolling_average_value(np.array(vals), ap)).tolist()
                if isinstance(_ap, float) or isinstance(_ap, int):
                    _ap = [_ap]
                self.__lines[key]['vals'] = _ap

    def __generate_regions(self):
        """Resolve regions.

        Parameters
        ----------
        xlower: float
            The lower bound to revoke linelists
        xupper: float
            The upper bound to revoke linelists

        """
        xlower, xupper = self.__config['xlower'], self.__config['xupper']
        self.remove_region(xlower=xlower, xupper=xupper)

    def __refresh(self):
        """Refresh all computations."""
        self.remove_lines([])
        self.__compute_aperture(line_agnostic = False)
        self.__generate_regions()

    @classmethod
    @property
    def return_types(self):
        """Return the types of line regions that have been defined."""
        return self.__types

    @classmethod
    @property
    def iterate_base_atomiclines(self):
        """Return all lines."""
        return self.__base_atomiclines.items()

    @property
    def return_lines(self):
        """Return all lines."""
        return frozendict(**self.__lines)

    @property
    def return_config(self):
        """Return lines within the region."""
        return frozendict(**self.__config)

    def return_labels(self):
        """Return all labels.

        mindistance: float
            The minimum distance between labels in units of the labels
        """
        labels = {}
        keys = list(self.__lines.keys())
        for k, v in self.__lines.items():
            labels[k] = v['vals']
        return labels

    def reset(self):
        """."""
        self.__reset()

    def refresh(self):
        """."""
        self.__refresh()

    @classmethod
    def strip_name(cls, name: str):
        name = name.replace('-', '')\
                   .replace('_', '')\
                   .replace('(', '')\
                   .replace(')', '')\
                   .replace('\\', '')\
                   .replace('+', '')\
                   .replace('=', '')\
                   .replace(' ', '')
        return name.lower()

    @classmethod
    def is_line(cls, linename: str):
        """Resolve Band."""
        linename = cls.strip_name(linename)
        for b in cls.__types:
            for line in base_lines[b]:
                if linename == cls.strip_name(line):
                    return True

        return False

    @classmethod
    def resolve_band(cls, band: str):
        """Resolve Band."""
        band = band.lower()
        if band not in cls.__types:
            return 'nir'
        else:
            return band

    def aperture(self, ap: float = None, line_agnostic: bool=False):
        """Apply a window.

        Applies a 'window' across all lines.
        A line list: [2.16, 2.17, 0.9, 1.4, 1.41]
        with ap: 0.2
        will yield: [2.165, 0.9, 1.405]

        This will add a new dict key: val
        to the requestable linelist. It is
        available under the 'aperture' key.

        Parameters
        ----------
        ap: float, optional
            set the aperture window size,
                if None or <=0 will remove aperture, default is None

        """
        self.__config['aperture'] = ap
        self.__compute_aperture(line_agnostic)
        self.__generate_regions()
        return self

    def remove_lines(self, linenames: list, remove_all: bool = False):
        """Remove the list of lines from output.

        This works by adding ut to the __regions dict.

        Parameters
        ----------
        linenames: list
            The List[str] of linenames to remove.

        """
        if len(self.__config['remove_lines']) > 0:
            self.__config['remove_lines'] = self.__config['remove_lines']\
                .union(set(linenames))
        else:
            self.__config['remove_lines'] = set(linenames)
        for line in (self.__config['remove_lines'] if not remove_all else self.__lines):
            if line in self.__config['allowed_lines']:
                continue
            if line in self.__lines:
                del self.__lines[line]
        return self

    def add_lines(self, linenames: list):
        """Add the list of lines to output.

        Overrides removal

        This works by adding ut to the __regions dict.

        Parameters
        ----------
        linenames: list
            The List[str] of linenames to add.

        """
        if len(self.__config['allowed_lines']) > 0:
            self.__config['allowed_lines'] = self.__config['allowed_lines']\
                .union(set(linenames))
        else:
            self.__config['allowed_lines'] = set(linenames)
        for line in self.__config['allowed_lines']:
            if line in self.__config['remove_lines']:
                self.__config['remove_lines'].remove(line)
        self.__populate_lines()
        self.__refresh()
        return self

    def remove_regions(self, limits):
        """Remove several regions.

        A nice wrapper function to quickly remove several defined
        regions. limits is 2d list.

        Parameters
        ----------
        limits: List[floats]
            A list with 2 parameters of floats.

        """
        for x in limits:
            self.remove_region(*x)

    def remove_region(self, xlower: float, xupper: float):
        """Remove a region.

        Parameters
        ----------
        xlower: float
            The lower bound to revoke linelists
        xupper: float
            The upper bound to revoke linelists

        """
        xlower, xupper = (xlower, xupper) if xlower < xupper else (xupper, xlower)
        if (xlower == -1 or xlower is None) and (xupper == -1 or xupper is None):
            return
        if xupper == -1 or xupper is None:
            xupper = np.inf
        if xlower == -1 or xlower is None:
            xlower = -np.inf

        keys = [k for k in self.__lines.keys()]
        allvals = [[key_i, v] for key_i, key_name in enumerate(keys) for v in self.__lines[key_name]['vals']]
        allvals = np.array(allvals, dtype=float)
        mask = allvals[:, 1] > xlower
        mask *= allvals[:, 1] < xupper
        allvals = allvals[mask, :].tolist()
        ret = {}
        for i in range(len(allvals)):
            keyname = keys[int(allvals[i][0])]
            if keyname in ret:
                ret[keyname].append(allvals[i][-1])
            else:
                ret[keyname] = [allvals[i][-1]]
        for kn in keys:
            if kn in ret:
                self.__lines[kn]['vals'] = ret[kn]
            else:
                del self.__lines[kn]


def test():
    # List of atomic lines to ignore. The function isn't that intelligent so try to give as accurate a name as possible.
    xlim = (0.9, 2.4)  # limit to plot
    telluric = [[-1, 2.0], [2.4, -1]]  # additional telluric lines to remove
    lines_to_ignore = ['all', ]
    allowed_lines = [r'Br $\gamma$',
                     'CO', 'Fe II', 'Fe I', 'He I', 'K I',
                     r'Pa $\alpha$', r'Pa $\beta$', r'Pa $\gamma$',
                     r'Fe$_2$ a4d7-a4d9',
                     r'H$_2$ $\nu$=1-0 S(0)',
                     r'H$_2$ $\nu$=1-0 S(1)',
                     r'H$_2$ $\nu$=1-0 S(2)',
                     r'H$_2$ $\nu$=1-0 S(3)',
                     r'H$_2$ $\nu$=2-1 S(1)',
                     r'H$_2$ $\nu$=3-2 S(4)',
                     r'H$_2$ $\nu$=2-1 S(2)',
                     r'H$_2$ $\nu$=2-1 S(3)',
                     r'H$_2$ $\nu$=2-1 S(5)',
                     r'H$_2$ $\nu$=3-2 S(5)',
                     r'H$_2$ $\nu$=3-2 S(7)',
                     r'H$_2$ $\nu$=3-2 S(3)']

    # Check no removes have been made
    lingentotal = Lines(band='nir')
    baselines = dict([[k[0], k[-1]['val']] for k in lingentotal.iterate_base_atomiclines])
    totalbaselines = [v for k, vs in baselines.items() for v in vs]
    if len(lingentotal.return_lines) != len(lingentotal.iterate_base_atomiclines):
        raise Exception('Initilization is incorrect and removing lines')
    lingentotal = Lines(band='nir', unit='microns')
    if len(lingentotal.return_lines) != len(lingentotal.iterate_base_atomiclines):
        raise Exception('Initilization is incorrect and removing lines')
    # Check proper selection
    lingentotal = Lines(band='nir', unit='microns',
                        xlower=xlim[0],
                        xupper=xlim[1])
    lines = lingentotal.return_lines
    totallines = np.array([v for k in lines for v in lines[k]['vals']], dtype=float)
    if any(totallines > xlim[1]) + any(totallines < [0]):
        raise Exception('Xlimits not properly selecting')
    # Check exclusion of all
    lingentotal = Lines(band='nir', unit='microns',
                        xlower=xlim[0],
                        xupper=xlim[1],
                        remove_lines=lines_to_ignore)
    lines = lingentotal.return_lines
    if len(lines) != 0:
        raise Exception(f'Remove lines not working. {lines}')
    # Check exclusion of all + inclusion of few
    lingentotal = Lines(band='nir', unit='microns',
                        xlower=xlim[0],
                        xupper=xlim[1],
                        remove_lines=lines_to_ignore,
                        allowed_lines=allowed_lines)
    if len(lingentotal.return_lines) != len(allowed_lines):
        raise Exception('Allowed lines not properly setting.')
    # Check call aperture in init
    lingentotal = Lines(band='nir', unit='microns',
                        xlower=xlim[0],
                        xupper=xlim[1],
                        aperture=1.5e-2,
                        remove_lines=lines_to_ignore,
                        allowed_lines=allowed_lines)
    lines = lingentotal.return_lines
    totallines = [v for k in lines for v in lines[k]]
    if len(lines['K I']) >= len(baselines['K I']):
        raise Exception('Aperture not reducing properly')
    # Check call aperture after
    lingentotal = Lines(band='nir', unit='microns',
                        xlower=xlim[0],
                        xupper=xlim[1]).remove_regions(telluric)
    lines = lingentotal.return_lines
    totallines = [v for k in lines for v in lines[k]]
    lingentotal.aperture(1.5e-2)
    lines = lingentotal.return_lines
    totallines = [v for k in lines for v in lines[k]]
    if len(lines['K I']) >= len(baselines['K I']):
        raise Exception('Aperture not reducing properly')
    # Check call aperture after, huge
    lingentotal = Lines(band='nir', unit='microns',
                        xlower=xlim[0],
                        xupper=xlim[1]).remove_regions(telluric)
    lines = lingentotal.return_lines
    totallines = [v for k in lines for v in lines[k]]
    lingentotal.aperture(10)
    lines = lingentotal.return_lines
    totallines = [v for k in lines for v in lines[k]]
    if len(lines['K I']) >= len(baselines['K I']):
        raise Exception('Aperture not reducing properly')

__doc__ = Lines.__doc__

if __name__ == '__main__':
    test()

# end of code

# end of file
