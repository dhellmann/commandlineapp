#
# $Id$
#

SVNHOME=$(shell svn info | grep "^URL" | cut -f2- -d:)
PROJECT=$(shell basename $(shell dirname $(SVNHOME)))
VERSION=$(shell basename $(SVNHOME))
RELEASE=$(PROJECT)-$(VERSION)

info:
	@echo SVNHOME=$(SVNHOME)
	@echo PROJECT=$(PROJECT)
	@echo VERSION=$(VERSION)
	@echo
	@echo "package - create the tarball"
	@echo "register - update PyPI"
	@echo

package: setup.py
	python setup.py sdist --force-manifest
	mv dist/*.tar.gz ~/Desktop/

register: setup.py
	python setup.py register

%: %.in
	rm -f $@
	cat $< | sed 's/VERSION/$(VERSION)/g' > $@
	chmod -w $@

tags:
	find . -name '*.py' | etags -l auto --regex='/[ \t]*\def[ \t]+\([^ :(\t]+\)/\1/' -
