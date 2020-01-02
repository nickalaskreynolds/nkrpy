"""Hold units for Unit class."""
from ..constants import ev, pi

__all__ = ('units',)

units = {
    # energy
    'j': {'vals': ('j', 'joules', 'joule'),
          'type': 'energy',
          'name': 'j',
          'fac': 1.},
    'ev': {'vals': ('ev', 'electronvolt', 'evs', 'electronvolts'),
           'type': 'energy',
           'name': 'ev',
           'fac': ev},
    'kev': {'vals': ('kev', 'kiloelectronvolt', 'kevs',
                     'kiloelectronvolts', 'kiloev'),
            'type': 'energy',
            'name': 'kev',
            'fac': 1.E3 * ev},
    'mev': {'vals': ('mev', 'megaelectronvolt', 'mevs',
                     'megaelectronvolts'),
            'name': '',
            'type': 'energy',
            'fac': 1.E6 * ev},
    'gev': {'vals': ('gev', 'gigaaelectronvolt', 'gevs', 'gigaelectronvolts'),
            'name': 'gev',
            'type': 'energy',
            'fac': 1.E9 * ev},
    # angles
    'degrees': {'vals': ('deg', 'd', 'degree'),
                'name': 'degrees',
                'type': 'angle',
                'fac': 3600.},
    'hourangle': {'vals': ('ha', 'hourangles'),
                  'name': 'hourangle',
                  'type': 'angle',
                  'fac': 3600. * 15.},
    'arcmin': {'vals': ('am', 'arcmins'),
               'name': 'arcmin',
               'type': 'angle',
               'fac': 60.},
    'arcsec': {'vals': ('as', 'arcsecs'),
               'name': 'arcsec',
               'type': 'angle',
               'fac': 1.},
    'radians': {'vals': ('rad', 'radian', 'rads'),
                'name': 'radians',
                'type': 'angle',
                'fac': 3600. * 180. / pi},
    # coordinate transformation
    'xyz': {'vals': ('cartesian', 'cart',),
            'name': 'xyz',
            'type': 'coord',
            'fac': None},
    'sph': {'vals': ('spherical', 'rtp', 'sphere'),
            'name': 'sph',
            'type': 'coord',
            'fac': None},
    'cyl': {'vals': ('cylindrical', 'rtz',),
            'name': 'cyl',
            'type': 'coord',
            'fac': None},
    # astronomical transofrmations
    'gal': {'vals': ('galactic', 'lb',),
            'name': 'gal',
            'type': 'astro',
            'fac': None},
    'j2000': {'vals': ('j2000',),
              'name': 'j2000',
              'type': 'astro',
              'fac': None},
    'b1950': {'vals': ('1950', 'j1950',),
              'name': 'b1950',
              'type': 'astro',
              'fac': None},
    'helio': {'vals': ('sun', 'heliocentric',),
              'name': 'helio',
              'type': 'astro',
              'fac': None},
    # distance
    'bananas': {'vals': ('b', 'banana'),
                'name': 'bananas',
                'type': 'wave',
                'fac': 2.032 * 10 ** 9},
    'angstroms': {'vals': ('ang', 'a', 'angs', 'angstrom'),
                  'name': 'angstroms',
                  'type': 'wave',
                  'fac': 1.},
    'micrometers': {'vals': ('microns', 'micron', 'mu', 'micrometres',
                             'micrometre', 'micrometer'),
                    'name': 'micrometers',
                    'type': 'wave',
                    'fac': 10 ** 4},
    'millimeters': {'vals': ('mm', 'milli', 'millimetres',
                             'millimetre', 'millimeter'),
                    'name': 'millimeters',
                    'type': 'wave',
                    'fac': 10 ** 7},
    'centimeters': {'vals': ('cm', 'centi', 'centimetres',
                             'centimetre', 'centimeter'),
                    'name': 'centimeters',
                    'type': 'wave',
                    'fac': 10 ** 8},
    'meters': {'vals': ('m', 'metres', 'meter', 'metre'),
               'name': 'meters',
               'type': 'wave',
               'fac': 10 ** 10},
    'kilometers': {'vals': ('km', 'kilo', 'kilometres', 'kilometre',
                            'kilometer'),
                   'name': 'kilometers',
                   'type': 'wave',
                   'fac': 10 ** 13},
    'lightyear': {'vals': ('lyr', 'lightyears'),
                  'name': 'lightyear',
                  'type': 'wave',
                  'fac': 9.461E25},
    'parcsec': {'vals': ('pc', 'parsecs'),
                'name': 'parcsec',
                'type': 'wave',
                'fac': 3.086E26},
    # frequency
    'hz': {'vals': ('hertz', 'h'),
           'name': 'hz',
           'type': 'freq',
           'fac': 1.},
    'khz': {'vals': ('kilohertz', 'kilo-hertz', 'kh'),
            'name': 'khz',
            'type': 'freq',
            'fac': 10 ** 3},
    'mhz': {'vals': ('megahertz', 'mega-hertz', 'mh'),
            'name': 'mhz',
            'type': 'freq',
            'fac': 10 ** 6},
    'ghz': {'vals': ('gigahertz', 'giga-hertz', 'gh'),
            'name': 'ghz',
            'type': 'freq',
            'fac': 10 ** 9},
    'thz': {'vals': ('terahertz', 'tera-hertz', 'th'),
            'name': 'thz',
            'type': 'freq',
            'fac': 10 ** 12},
}

# end of code

# end of file
