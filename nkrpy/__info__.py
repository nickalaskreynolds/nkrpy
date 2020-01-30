# flake8: noqa
# This file is auto-generated from the setup.py file.
name = """nkrpy"""
description = """Originally was just a collection of python programs that I 

    found myself using repeatidly. Migrating a lot of more

    efficient modules and made more general.



If you would like to run the development version, please pull

    from the github instead as the pypi distribution excludes

    the docs, tests, and other potentially useful things.
"""
long_description = """Originally was just a collection of python programs that I 

    found myself using repeatidly. Migrating a lot of more

    efficient modules and made more general.



If you would like to run the development version, please pull

    from the github instead as the pypi distribution excludes

    the docs, tests, and other potentially useful things.
"""
long_description_content_type = """text/md"""
version = """0.1"""
url = """http://github.com/nickalaskreynolds/nkrpy"""
author = """Nickalas Reynolds"""
author_email = """email@nickreynolds.xyz"""
license = """MPL2.0"""
packages = ['nkrpy', 'nkrpy.image', 'nkrpy.misc', 'nkrpy.astro', 'nkrpy.io', 'nkrpy.amlines', 'nkrpy.publication', 'nkrpy.math', 'nkrpy.unit', 'nkrpy.logger', 'nkrpy.astro.observing', 'nkrpy.astro.dustmodels', 'nkrpy.astro.reduction', 'nkrpy.astro.mercury', 'nkrpy.astro.reduction.arcsat', 'nkrpy.io.fits', 'nkrpy.math.gp', 'tests.image', 'tests.misc', 'tests.astro', 'tests.io', 'tests.amlines', 'tests.math', 'tests.unit', 'tests.logger']
scripts = ['./bin/template', './bin/outlinegen.py', './bin/docgen.sh', './bin/misc/newPVPlot.py', './bin/misc/submit_jobs.py', './bin/misc/make_line_image.py', './bin/misc/deprojection.py', './bin/misc/QL_ARCSAT.py', './bin/misc/script.py', './bin/misc/matplotlib_colors.py', './bin/misc/jt_mass_c17o.py', './bin/misc/paul_bootstrap.py', './bin/misc/arcsat_nightlog_creator.sh', './bin/misc/fft_h370_example.ipynb', './bin/misc/tspec_analysis/template_analysis.ipynb', './bin/misc/tspec_analysis/README.md', './bin/misc/tspec_analysis/.ipynb_checkpoints/template_analysis-checkpoint.ipynb', './bin/templates/template.py', './bin/templates/template.sh', './bin/templates/template.rst', './bin/templates/template.md']
zip_safe = True
include_package_data = True
ext_modules = [<setuptools.extension.Extension('nkrpy.image.centering') at 0x7f32a0859f50>, <setuptools.extension.Extension('nkrpy.image.image_interp') at 0x7f32a0859d10>, <setuptools.extension.Extension('nkrpy.astro.keplerian') at 0x7f32a084ec90>, <setuptools.extension.Extension('nkrpy.math.sampler') at 0x7f32a085fc50>, <setuptools.extension.Extension('nkrpy.math.image') at 0x7f32a0868590>, <setuptools.extension.Extension('nkrpy.math.miscmath') at 0x7f32a084eb10>, <setuptools.extension.Extension('nkrpy.math.fit') at 0x7f32a0859710>, <setuptools.extension.Extension('nkrpy.math.vector') at 0x7f32a0804210>, <setuptools.extension.Extension('nkrpy.unit.unit') at 0x7f32a08043d0>, <setuptools.extension.Extension('nkrpy.unit.convert') at 0x7f32a0859bd0>]
install_requires = ['APLpy==1.1.1', 'astropy==3.0.4', '#astropy-healpix>=0.4', 'corner>=2.0.1', 'Cython>=0.29.14', 'emcee>=2.2.1', '#fits2hdf>=1.1.1', 'flake8>=3.7.8', '#GPy>=1.9.9', '#h5py>=2.10.0', 'matplotlib>=3.1.1', '#mpi4py>=3.0.3', 'numpy>=1.17.4', '#pdspy>=1.0.0', '#Pillow>=6.2.0', 'pytest>=5.2.1', '#radio-beam>=0.3.2', 'scipy>=1.3.3', 'sklearn>=0.0', 'Sphinx>=2.2.0', 'rst2pdf>=0.95']
py_modules = []
classifiers = ['Development Status :: 4 - Beta', 'License :: OSI Approved :: aikolsuaklsdjklasjdklasjdkljaskldjMozilla Public License 2.0 (MPL 2.0)', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: 3 :: Only', 'Intended Audience :: Developers', 'Natural Language :: English']
