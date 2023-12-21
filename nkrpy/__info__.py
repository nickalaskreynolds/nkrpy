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
author = """Nickalas Reynolds Tran"""
author_email = """email@nickreynolds.xyz"""
license = """MPL2.0"""
packages = ['nkrpy', 'nkrpy.misc', 'nkrpy.astro', 'nkrpy.io', 'nkrpy._math', 'nkrpy.publication', 'nkrpy._unit', 'nkrpy.astro.observing', 'nkrpy.astro.plot', 'nkrpy.astro.dust', 'nkrpy.astro._pvdiagram', 'nkrpy.astro.models', 'nkrpy.astro._atomiclines', 'nkrpy.astro.plot.arcsat', 'nkrpy.io._logger', 'nkrpy._math.gp', 'tests.image', 'tests.misc', 'tests.astro', 'tests.io', 'tests.amlines', 'tests.math', 'tests.unit', 'tests.logger']
scripts = ['./bin/template', './bin/docker_cheatsheet', './bin/checkjobs', './bin/outlinegen.py', './bin/make_uv_1d.py', './bin/latexstrip.py', './bin/apoexpcal.pro', './bin/docgen.sh', './bin/misc/newPVPlot.py', './bin/misc/submit_jobs.py', './bin/misc/example_reduc.py', './bin/misc/make_line_image.py', './bin/misc/deprojection.py', './bin/misc/QL_ARCSAT.py', './bin/misc/script.py', './bin/misc/matplotlib_colors.py', './bin/misc/jt_mass_c17o.py', './bin/misc/paul_bootstrap.py', './bin/misc/casa_deproj_vis.py', './bin/misc/alma_reduc_misc.py', './bin/misc/arcsat_nightlog_creator.sh', './bin/misc/fft_h370_example.ipynb', './bin/misc/tspec_analysis/template_analysis.ipynb', './bin/misc/tspec_analysis/README.md', './bin/misc/tspec_analysis/.ipynb_checkpoints/template_analysis-checkpoint.ipynb', './bin/templates/template.py', './bin/templates/template.sh', './bin/templates/template.rst', './bin/templates/template.md']
include_package_data = True
ext_modules = [<setuptools.extension.Extension('nkrpy.misc.constants') at 0x7fe62de80130>, <setuptools.extension.Extension('nkrpy.astro.models._flareddiskmodel') at 0x7fe62de80a60>, <setuptools.extension.Extension('nkrpy._math._image') at 0x7fe62d773e50>, <setuptools.extension.Extension('nkrpy._math._convert') at 0x7fe62d80fee0>, <setuptools.extension.Extension('nkrpy._math._fit') at 0x7fe62d810520>, <setuptools.extension.Extension('nkrpy._math._miscmath') at 0x7fe62d810d00>, <setuptools.extension.Extension('nkrpy._math._triangle') at 0x7fe62d804490>, <setuptools.extension.Extension('nkrpy._math._vector') at 0x7fe62d8102e0>, <setuptools.extension.Extension('nkrpy._math._sampler') at 0x7fe62d804910>, <setuptools.extension.Extension('nkrpy._unit.unit') at 0x7fe62d7f4160>, <setuptools.extension.Extension('nkrpy._unit._base') at 0x7fe62d7f47f0>]
install_requires = ['APLpy==1.1.1', 'astropy==3.0.4', '#astropy-healpix>=0.4', 'corner>=2.0.1', 'Cython>=0.29.14', 'cmasher>=1.2.2', 'emcee>=2.2.1', '#fits2hdf>=1.1.1', '#flake8>=3.7.8', '#GPy>=1.9.9', '#h5py>=2.10.0', 'matplotlib>=3.1.1', '#mpi4py>=3.0.3', 'numpy>=1.17.4', '#pdspy>=1.0.0', '#Pillow>=6.2.0', 'pytest>=5.2.1', '#radio-beam>=0.3.2', 'scipy>=1.3.3', 'sklearn>=0.0', '#Sphinx>=2.2.0', '#rst2pdf>=0.95']
py_modules = []
classifiers = ['Development Status :: 4 - Beta', 'License :: OSI Approved :: aikolsuaklsdjklasjdklasjdkljaskldjMozilla Public License 2.0 (MPL 2.0)', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: 3 :: Only', 'Intended Audience :: Developers', 'Natural Language :: English']
zip_safe = True
