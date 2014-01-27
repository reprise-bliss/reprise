all: reprise.egg-info

reprise.egg-info:
	python3 setup.py egg_info

test: all
	python3 setup.py test

coverage: clean
	coverage3 run --source=. setup.py test
	coverage3 html
	coverage3 report

pep8:
	pep8 .

deb: clean-all
	dpkg-buildpackage -b -us -uc -tc
	lintian --pedantic ../reprise_*.deb ../reprise_*.changes

ifdef DEB_HOST_ARCH
install:
	@python3 setup.py install --no-compile \
	    --prefix="usr/" --root="$(DESTDIR)" \
	    --install-layout=deb
endif

clean:
	rm -rf reprise.egg-info reprise/__pycache__/
	rm -rf build/ .coverage htmlcov/

clean-all: clean
	rm -rf ../reprise_*.deb ../reprise_*.changes
