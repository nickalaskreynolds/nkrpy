"""The setup.py file for building the NKRPY module."""
# internal modules
from setuptools import setup, find_packages, Extension
import os
import importlib
import inspect
import glob

# external modules
from Cython.Build import cythonize
import numpy

# global attributes
__filename__ = __file__.split('/')[-1].strip('.py')
__path__ = __file__.strip('.py').strip(__filename__)
sep = os.sep

supported = {'pyx': 1,
             'f90': 2,
             'c': 3, 'i': 4}  # supported extensions
supported_inverse = dict((v, k) for k, v in supported.items())


# populate the __info__ and __init__ files
def populate_info(kwargs: dict) -> None:
    """Populate the info of the package dunders.

    This file will read call in the settings that are passed into the setup
        for disutils and populate a __info__ and __init__ dunder method.
        Reads from the __init_generator__.py in addition to the above settings
        to generate the __init__.py
    """
    with open(f'__auto_generated_setup_info.txt', 'w') as f:
        for key, val in kwargs.items():
            f.write(f'{key.ljust(25)} = {val}\n')

    with open(f'nkrpy{sep}__info__.py', 'w') as f:
        f.write('# flake8: noqa\n')
        f.write('# This file is auto-generated from the setup.py file.\n')
        for key, val in kwargs.items():
            if isinstance(val, str):
                f.write(f'{key} = """{val}"""\n')
            if isinstance(val, (bool, int, float)):
                f.write(f'{key} = {val}\n')
            if isinstance(val, list):
                f.write(f'{key} = {val}\n')

    # read generator
    with open(f'nkrpy{sep}__init_generator__.py', 'r') as f:
        alllines = f.readlines()
    string = [kwargs['description']]
    app = 'This file is autogenerated by setup.py'
    string.append(f'\n{"=" * len(app)}\n{app}\n{"=" * len(app)}\n')
    string = '\n'.join(string)
    alllines[0] = alllines[0].replace('DESC', 'nkrpy.\n' + string)
    alllines = ''.join(alllines)
    # actually write the __init__ file
    f = open(f'nkrpy{sep}__init__.py', 'w')
    f.write(alllines)
    f.flush()
    f.close()
    pass


# gather/handle all extensions
def load_ext(extname: str, files: list, fext: str) -> tuple:
    """Resolve extension from files.

    Parameters
    ----------
    extname: str
        name of the extension to use
    files: List[str]
        list of the files to include in the extension
    fext: str
        The extension (w/o '.') of the file

    Returns
    -------
    ext: setuptools.Extension
        The extension object that has been resolved
    pym: str
        The python module name if header interfaces are defined
    """
    pym = None
    print(extname, files)
    if fext == 'pyx':
        ext = cythonize(Extension(extname, files,
                                  include_dirs=[numpy.get_include()],
                                  libraries=[], library_dirs=[],
				 ),
                        language_level='3')[0]
    elif fext == 'f90':
        ext = Extension(extname, files, include_dirs=[],
                        libraries=[], library_dirs=[])
    elif fext == 'c':
        ext = Extension(extname, files, include_dirs=[],
                        libraries=[], library_dirs=[])
    elif fext == 'i':
        ext = Extension(extname, files, include_dirs=[],
                        libraries=[], library_dirs=[],
                        swig_opts=['-modern', '-I../include'])
        pym = f'_{extname}'
    return ext, pym


def resolve(files: list) -> list:
    f"""Resolve filenames in heirarchical order.

    This is based on the "{supported}" heirarchy, where lower numbers override higher ones.
    """
    def get_ext(ext: str) -> int:
        """Get the extension for a filename."""
        try:
            if ext not in supported:
                return -1
            return supported[ext]
        except Exception:
            return -1

    def get_fname_ext(f: str) -> str:
        ext = f.split('.')[-1]
        return f.replace(f'.{ext}', ''), ext, get_ext(ext)

    _t = [get_fname_ext(f) for f in files]
    _t.sort(key=lambda x: x[2])
    _s = set()
    ret = []
    for f in _t:
        if f[0] in _s:
            continue
        ret.append(f)
        _s.update([f[0]])
    return ret


# need to delete all __pycache__
for root, dirs, files in os.walk('./'):
    for d in dirs:
        if d == '__pycache__':
            os.system(f'rm -rf {os.path.join(root, d)}')

extensions = []  # hold all exts
py_modules = []  # hold any aggregates from SWIGs
# walk through all files
aggregate = []
for path, dirnames, filenames in os.walk(f'.{sep}nkrpy{sep}'):
    for filename in filenames:
        if filename.startswith('__'):
            continue
        if filename.split('.')[-1] not in supported:
            continue
        x = os.sep.join([path, filename]).replace(f'{sep}{sep}', sep)
        aggregate.append(x)
aggregate = resolve(aggregate)
for f in aggregate:
    fname = f[0].strip('.').replace(sep, '.').strip('.')
    print(fname, [f'{f[0]}.{f[1]}'], f[1])
    ext, pym = load_ext(fname, [f'{f[0]}.{f[1]}'], f[1])
    if ext is not None:
        extensions.append(ext)
    if pym is not None:
        py_modules.append(pym)

# The below is used to populate the settings dictionary to pass for
# building of the dunders and into `setuptools.setup`
# gather all scripts
scripts = []
for path, dirnames, filenames in os.walk(f'.{sep}bin{sep}'):
    for file in filenames:
        fext = file.split('.')[-1]
        file = os.path.join(path, file)
        #print(file)
        scripts.append(file)

# read .version
with open(os.path.join(os.path.dirname(__file__), '.version')) as v:
    version = v.read()

# read README
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as r:
    skiprows = 4
    readme = r.readlines()
    readme = '\n'.join(readme[skiprows:])

# read requirements
with open(os.path.join(os.path.dirname(__file__),
          'requirements.txt')) as req:
    requirements = req.read().splitlines()

# define package data
package_data = {
    'META': ['LICENSE', 'README.md', 'requirements.txt', '.version'],
    'DATA': glob.glob('nkrpy/*.tbl') + glob.glob('nkrpy/*.dat'),
    'TESTS': ['tests'],
    'EXAMPLES': ['examples'],
}

# the general settings handler
settings = {
    'name': 'nkrpy',
    'description': readme,
    'long_description': readme,
    'long_description_content_type': "text/md",
    'version': version,
    'url': 'http://github.com/nickalaskreynolds/nkrpy',
    'author': 'Nickalas Reynolds Tran',
    'author_email': 'email@nickreynolds.xyz',
    'license': 'MPL2.0',
    'packages': find_packages(exclude=['tests', 'docs', 'examples']),
    'scripts': scripts,
    'include_package_data': True,
    'package_data': package_data,
    'ext_modules': extensions,
    'install_requires': requirements,
    'py_modules': py_modules,
    'classifiers': [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: aikolsuaklsdjklasjdklasjdkljaskldj' +
            'Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Intended Audience :: Developers',
        'Natural Language :: English'
    ],
    "zip_safe": True,
}


def print_settings(s):
    print(64*'#')
    print(' Setup Settings '.upper().center(64, '#'))
    print(64*'#')
    for k,v in s.items():
        print(str(k).center(64, '-'))
        print(str(v).center(64, ' '))
    print(64*'#')
    print(' END '.upper().center(64, '^'))
    print(64*'#')

if __name__ == '__main__':
    # now pass into the main functions
    populate_info(settings)

    # actually build
    setup(**settings)
    print_settings(settings)

# end of code

# end of file
