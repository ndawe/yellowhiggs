#!/usr/bin/env python

import os
import sys
from glob import glob


if os.getenv('YELLOWHIGGS_NO_DISTRIBUTE') in ('1', 'true'):
    from distutils.core import setup
else:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

execfile('yellowhiggs/info.py')
open('version.txt', 'w').write(VERSION)

if os.getenv('YELLOWHIGGS_AFS_INSTALL') in ('1', 'true'):
    prefix = '/afs/cern.ch/atlas/software/tools/yellowhiggs'
else:
    prefix = 'etc/yellowhiggs'

if 'install' in sys.argv:
    print __doc__

setup(name='yellowhiggs',
      version=VERSION,
      description='Interface for the CERN Yellow Report',
      long_description=open('README.rst').read(),
      author='Noel Dawe',
      author_email='noel.dawe@cern.ch',
      url=URL,
      download_url=DOWNLOAD_URL,
      packages=['yellowhiggs'],
      data_files=[(prefix, ['version.txt'])],
      package_data={
          'yellowhiggs': ['dat/xs/7/*.txt',
                          'dat/xs/8/*.txt',
                          'dat/xs/14/*.txt',
                          'dat/br/*.txt'],
      },
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
