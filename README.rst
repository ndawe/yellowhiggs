.. -*- mode: rst -*-

About
-----

yellowhiggs provides an interface with Higgs production cross section and branching ratio data in the
CERN Yellow Report:

* `CERNYellowReportPageAt7TeV <https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt7TeV>`_
* `CERNYellowReportPageBR <https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR>`_


Automatic Installation
----------------------

Automatically install the latest version of yellowhiggs with
`pip <http://pypi.python.org/pypi/pip>`_::

    pip install --user yellowhiggs

or with ``easy_install``::

    easy_install --user yellowhiggs

Omit the ``--user`` for a system-wide installation (requires root privileges).

To upgrade an existing installation use the ``-U``
option in the ``pip`` or ``easy_install`` commands above.


Manual Installation
-------------------

Get the latest tarball on `PyPI <http://pypi.python.org/pypi/yellowhiggs/>`_

Untar and install (replace X appropriately)::

   tar -zxvf yellowhiggs-X.tar.gz
   cd yellowhiggs-X

To install yellowhiggs into your home directory
if using at least Python 2.6::

   python setup.py install --user

or with older Python versions::

   python setup.py install --prefix=~/.local


Usage
-----

An example of how to use yellowhiggs::

   >>> import yellowhiggs
   >>> 
   >>> yellowhiggs.xsbr(7, 130, 'vbf', 'bb')
   (0.5689219999999999, 0.584851816, 0.555836794)
   >>> 
   >>> yellowhiggs.xsbr(7, 130, 'vbf', 'tautau')
   (0.0632392, 0.0650098976, 0.06178469839999999)
   >>> 
   >>> yellowhiggs.xsbr(7, 125, 'ggf', 'gammagamma')
   (0.0350599, 0.0418965805, 0.0297658551)
   >>> 
   >>> yellowhiggs.xs(7, 150, 'vbf')
   (0.9617, 0.9895892999999999, 0.9405426)
   >>> 
   >>> yellowhiggs.br(150, 'tautau')
   0.0178
   >>> yellowhiggs.br(155, 'tautau')
   0.0105

Cross sections are returned in units of [pb].
`xs` returns the (central cross section, high value, low value) at a center-of-mass energy [TeV]
for a given Higgs mass [GeV] and production mode.
`br` returns the branching ratio at a given Higgs mass [GeV] for a decay channel.
`xsbr` returns the cross section times branching ratio at a center-of-mass energy [TeV]
for a given Higgs mass [GeV], production mode and decay channel.
