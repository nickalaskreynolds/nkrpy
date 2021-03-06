"""Unit conversion."""
# cython modules

# internal modules

# external modules
from numpy import ndarray
from numpy import array as np_array

# relative modules
from ..misc.functions import typecheck
from ..misc.constants import c as n_c  # imported as cgs
from ..misc.constants import kb as n_kb  # imported as cgs
from ..misc.constants import h  # imported as cgs
from ._unit import units
from . import convert as nkrpy__convert

# global attributes
__all__ = ('BaseUnit', 'Unit',)
__doc__ = """Convert supported units all to angstroms and hz
    to add new units have to correct self.__units and resolve_unit
    To setup, just initialize and call with units /  values to convert
    Holds values to quick accessing later

    Use Units.converting for info on how you are converting
    """
__filename__ = __file__.split('/')[-1].strip('.py')
__path__ = __file__.strip('.py').strip(__filename__)

cdef long c, kb
c = n_c * 1E8  # A/s
kb = n_kb * 1E-7  # SI


class BaseVals(object):
    def __new__(cls, vals):
        if isinstance(vals, ndarray):
            vals = vals
        elif typecheck(vals):
            vals = np_array(vals)
        elif checknum(vals):
            vals = np_array([vals])
        else:
            vals = None
        return vals


def checknum(num):
    try:
        _ = float(num)
        return True
    except Exception:
        return False


class BaseUnit(object):
    """Override typical dict classing."""

    def __init__(self, **entries):
        """Dunder."""
        self.__dict__.update(entries)

    def values(self):
        """Dunder."""
        return self.__dict__.values()

    def items(self):
        """Dunder."""
        return self.__dict__.items()

    def keys(self):
        """Dunder."""
        return self.__dict__.keys()

    def __iter__(self):
        """Dunder."""
        return self.__dict__.items().__iter__()

    def __getitem__(self, key):
        """Dunder."""
        return self.__dict__[key]

    def __next__(self):
        """Dunder."""
        pass

    def __setattr__(self):
        """Dunder."""
        pass

    def __delattr__(self):
        """Dunder."""
        pass


class Unit(object):
    """Convert between major unit types."""

    __units = BaseUnit(**units)

    def __init__(self, baseunit: str = None,
                 convunit: str = None, vals: BaseVals = None):
        """Dunder.

        Parameters
        ----------
        baseunit: str
            The base unit to convert from.
        convunit: str
            The unit to convert to. Not Required.
        vals: number | numpy.ndarray
            The numbers to convert. Not Required.

        """
        if isinstance(vals, Unit):
            vals = vals.get_vals()
        self.reset()
        vals = BaseVals(vals)
        if baseunit is not None:
            self.__current_unit = self.resolve_unit(baseunit)
        if self.__current_unit is None:
            raise UnitNotFound('Unable to resolve the base unit. ' +
                               f'Make sure it is found in {self.__units}')
        if convunit is not None:
            self.__final_unit = self.resolve_unit(convunit)
        if self.__final_unit is None:
            raise UnitNotFound('Unable to resolve the conversion unit. ' +
                               f'Make sure it is found in {self.__units}')
        if not (baseunit is None and convunit is None):
            self.__current_vals = vals
            self.__generate_vals(vals=vals)


    def __call__(self, convunit: str = None, vals: BaseVals = None):
        """Resolve various conditions.

        Allows repeat calls and inline calling of function.
        Main process to gather all files
        This returns object of itself. Use return functions to get needed items

        Parameters
        ----------
        unit: str
        vals: float | ndarray

        """
        vals = BaseVals(vals)
        if vals is None and convunit is None:
            return self.__final_vals
        elif convunit is not None and vals is not None:
            unit = self.resolve_unit(convunit)
            self.__final_unit = unit
            self.__current_vals = vals
        elif convunit is not None:
            unit = self.resolve_unit(convunit)
            vals = self.__current_vals
        return self.__conversion(finalunit=unit, vals=vals)

    def __getitem__(self, x):
        return self.get_vals()[x]

    def __repr__(self):
        """Dunder."""
        _t = self.__conversion()
        if typecheck(_t):
            return ', '.join(map(str, _t))
        else:
            return str(f'{_t}')

    def __format__(self, formatstr: str = 's'):
        """Dunder."""
        if formatstr == 's':
            return self.__repr__()
        if '.' in formatstr:
            fmt = '{0:' + formatstr + '}'
            return fmt.format(self.__format__('f'))
        if formatstr == 'f':
            return float(self.__repr__())
        if formatstr == 'd':
            return int(self.__repr__())

    def __abs__(self):
        """Dunder."""
        return abs(self.__final_vals)

    def __add__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return self.__final_vals + value

    def __radd__(self, *args, **kwargs):
        """Dunder."""
        return self.__add__(*args, **kwargs)

    def __sub__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return self.__final_vals - value

    def __rsub__(self, *args, **kwargs):
        """Dunder."""
        return self.__sub__(*args, **kwargs)

    def __divmod__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return self.__final_vals / value

    def __rdivmod__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return value / self.__final_vals

    def __truediv__(self, *args, **kwargs):
        """Dunder."""
        return self.__divmod__(*args, **kwargs)

    def __rtruediv__(self, *args, **kwargs):
        """Dunder."""
        return self.__rdivmod__(*args, **kwargs)

    def __mul__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return self.__final_vals * value

    def __rmul__(self, *args, **kwargs):
        """Dunder."""
        return self.__mul__(*args, **kwargs)

    def __pow__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return self.__final_vals ** value

    def __rpow__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return value ** self.__final_vals

    def __mod__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return self.__final_vals % value

    def __rmod__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return value % self.__final_vals

    def __floordiv__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return self.__final_vals // value

    def __rfloordiv__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return value // self.__final_vals

    def __int__(self):
        """Dunder."""
        return int(self.__final_vals)

    def __float__(self):
        """Dunder."""
        return float(self.__final_vals)

    def __gt__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return self.__final_vals > value

    def __lt__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return self.__final_vals < value

    def __le__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return self.__final_vals <= value

    def __eq__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return self.__final_vals == value

    def __ge__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return self.__final_vals >= value

    def __ne__(self, value):
        """Dunder."""
        if isinstance(value, Unit):
            value = value.__final_vals
        return self.__final_vals != value

    def debug(self):
        """General debug help."""
        print(f"""
            Current Unit: {self.__current_unit}\n
            Current Values: {self.__current_vals}\n
            Final Unit: {self.__final_unit}\n
            Final Values: {self.__final_vals}""")

    def reset(self):
        """Reset vals."""
        self.__current_unit = None
        self.__current_vals = None
        self.__final_vals = None
        self.__final_unit = None
        self.__units = BaseUnit(**units)

    def set_base_unit(self, unit: str):
        """Set the base unit, don't reset vals."""
        _tmp = self.resolve_unit(unit)
        self.__current_unit = _tmp
        self.__generate_vals()

    def set_final_unit(self, unit: str):
        """Set the base unit, don't reset vals."""
        _tmp = self.resolve_unit(unit)
        self.__final_unit = _tmp
        self.__generate_vals()

    def get_vals(self):
        """Get the final val."""
        return self.__final_vals

    def get_base_unit(self):
        """Get the base units."""
        return self.__current_unit

    def get_final_unit(self):
        """Get the final units."""
        return self.__final_unit

    def get_base_val(self):
        """Get the base val."""
        return self.__current_vals

    @classmethod
    def get_units(cls):
        """Return the units possible in the current setup."""
        return cls.__units.keys()

    @classmethod
    def get_units_verbose(cls):
        """Return the units possible in the current setup."""
        return cls.__units.items()

    @classmethod
    def resolve_unit(cls, unresolved_unit: str):
        """Resolve the name of the unit from known types."""
        unresolved_unit = str(unresolved_unit).lower()
        if unresolved_unit not in cls.get_units():
            for i in cls.get_units():
                if unresolved_unit in cls.__units[i]['vals']:
                    return cls.__units[i]
            return None
        else:
            return cls.__units[unresolved_unit]

    def __conversion(self, baseunit=None, finalunit=None, vals=None):
        """Return conversion factor needed.

        Parameters
        ----------
        ctype = current type (wavelength, frequency, energy)
        ftype = final type to resolve to (wavelength, frequency, energy)
        init is the initial unit
        fin is the final unit
        This assumes everything has already been resolved with units

        """
        if vals is None:
            vals = self.__current_vals
        # converting between common types (wavelength->wavelength)
        if baseunit is None:
            baseunit = self.__current_unit
        if finalunit is None:
            finalunit = self.__final_unit
        if baseunit is None or finalunit is None:
            return None
        ctype, ftype = baseunit['type'], finalunit['type']
        # handle coordinate and astronomial transformations
        if ctype in ('coords', 'astro'):
            if not (ctype == ftype):
                return None
            if ctype == 'coords':
                func = getattr(nkrpy__convert,
                               f"{baseunit['name']}2" +
                               f"{finalunit['name']}")
            if ctype == 'astro':
                func = getattr(nkrpy__convert,
                               f"{baseunit['name']}2" +
                               f"{finalunit['name']}")
            return func(vals)
        # converting between freq, wavelength, energy
        if ctype == ftype:
            scaled = vals * baseunit['fac']
        # converting from freq to wavelength
        elif ((ctype == 'freq') and (ftype == 'wave') or
              (ctype == 'wave') and (ftype == 'freq')):
            scaled = c / (vals * baseunit['fac'])
        elif (ctype == 'energy') and (ftype == 'freq'):
            scaled = vals * baseunit['fac'] / h
        elif (ctype == 'freq') and (ftype == 'energy'):
            scaled = h * vals * baseunit['fac']
        elif ((ctype == 'energy') and (ftype == 'wave') or
              (ctype == 'wave') and (ftype == 'energy')):
            scaled = h * c / (vals * baseunit['fac'])

        return scaled / finalunit['fac']

    def __generate_vals(self, unit=None, vals=None):
        """Convert the values appropriately.

        unit is the type _resolve_name output
        vals can be either single values or iterable.
        """
        if unit is not None:
            self.__final_unit = unit
        else:
            if self.__final_unit is None:
                self.__final_unit = self.__current_unit
        if vals is not None:
            # convert from cu to fu with vals
            self.__final_vals = self.__conversion(vals=vals)
        else:
            # convert from cu to fu with self.vals
            self.__final_vals = self.__conversion()


class UnitNotFound(Exception):
    def __init__(self, message, errors = None):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors

# end of code

# end of file
