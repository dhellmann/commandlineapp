#
# $Id$
#

PROJECT=CommandLineApp
VERSION=3.0.3
RELEASE=$(PROJECT)-$(VERSION)

info:
	@echo PROJECT=$(PROJECT)
	@echo VERSION=$(VERSION)
	@echo
	@echo "package - create the tarball"
	@echo "register - update PyPI"
	@echo

package: setup.py docs
	python setup.py sdist --force-manifest
	mv dist/*.tar.gz ~/Desktop/

docs: commandlineapp.py
	epydoc -v --docformat restructuredtext --output docs commandlineapp.py

register: setup.py
	python setup.py register

%: %.in
	rm -f $@
	cat $< | sed 's/VERSION/$(VERSION)/g' > $@

tags:
	find . -name '*.py' | etags -l auto --regex='/[ \t]*\def[ \t]+\([^ :(\t]+\)/\1/' -
