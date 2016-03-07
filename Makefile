# simple makefile to simplify repetitive build env management tasks under posix

PYTHON := $(shell which python)
NOSETESTS ?= nosetests

all: clean

clean-pyc:
	find . -name "*.pyc" -exec rm {} \;

clean-build:
	rm -rf build

clean: clean-build clean-pyc

install:
	$(PYTHON) setup.py install

install-user:
	$(PYTHON) setup.py install --user

sdist: clean
	$(PYTHON) setup.py sdist

register:
	$(PYTHON) setup.py register

upload: clean
	$(PYTHON) setup.py sdist upload

check-rst:
	python setup.py --long-description | rst2html.py > __output.html
	firefox __output.html
	rm -f __output.html

pep8:
	@pep8 --exclude=.git,extern yellowhiggs
