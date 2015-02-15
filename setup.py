#!/usr/bin/env python

import os
# Prevent distutils from trying to create hard links
# which are not allowed on AFS between directories.
# This is a hack to force copying.
try:
    del os.link
except AttributeError:
    pass

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys
from glob import glob

execfile('yellowhiggs/info.py')

if 'install' in sys.argv:
    print __doc__

setup(
    name='yellowhiggs',
    version=__version__,
    description='Interface for the CERN Yellow Report',
    long_description=open('README.rst').read(),
    author='Noel Dawe',
    author_email='noel.dawe@cern.ch',
    url=URL,
    download_url=DOWNLOAD_URL,
    packages=['yellowhiggs'],
    package_data={
        'yellowhiggs': [
            'dat/xs/7/*.txt',
            'dat/xs/8/*.txt',
            'dat/xs/13/*.txt',
            'dat/xs/14/*.txt',
            'dat/br/*.txt',
        ],
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
    ])
