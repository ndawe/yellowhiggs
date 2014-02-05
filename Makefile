# simple makefile to simplify repetitive build env management tasks under posix

PYTHON := $(shell which python)
NOSETESTS ?= nosetests

all: clean

clean-pyc:
	find . -name "*.pyc" -exec rm {} \;

clean-build:
	rm -rf build

clean-distribute:
	rm -f distribute-*.egg
	rm -f distribute-*.tar.gz

clean: clean-build clean-pyc clean-distribute

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

trailing-spaces:
	find yellowhiggs -name "*.py" | xargs perl -pi -e 's/[ \t]*$$//'

update-distribute:
	curl -O http://python-distribute.org/distribute_setup.py

check-rst:
	python setup.py --long-description | rst2html.py > __output.html
	firefox __output.html
	rm -f __output.html

pep8:
	@pep8 --exclude=.git,extern yellowhiggs
