#!/usr/bin/env python

import os
import sys


if os.getenv('YELLOWHIGGS_NO_DISTRIBUTE') in ('1', 'true'):
    from distutils.core import setup
    packages = ['yellowhiggs']
else:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    packages = find_packages()

execfile('yellowhiggs/info.py')
open('version.txt', 'w').write(VERSION)

if os.getenv('YELLOWHIGGS_AFS_INSTALL') in ('1', 'true'):
    prefix = '/afs/cern.ch/atlas/software/tools/yellowhiggs'
else:
    prefix = 'etc/yellowhiggs'

if 'install' in sys.argv:
    print __doc__

setup(name='pyAMI',
      version=VERSION,
      description='Interface for the CERN Yellow Report',
      long_description=open('README.rst').read(),
      author='Noel Dawe',
      author_email='noel.dawe@cern.ch',
      url=URL,
      download_url=DOWNLOAD_URL,
      packages=packages,
      data_files=[(prefix, ['version.txt'])],
      license='GPLv3',
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Utilities",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)"
      ]
     )

os.unlink('version.txt')
