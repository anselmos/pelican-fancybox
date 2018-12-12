
# Makefile

all:
	@echo All done, in fact, there was nothing to build ...

test:
	pytest -v test_fancybox.py

pep8:
	flake8 \
	    --max-line-length=131 \
	    --statistics \
	    *.py

install:
	@echo What to install is undocumented, a.k.a. TODO

clean:
	# inspired by .gitignore
	rm -fr __pycache__/
	rm -f *.py[cod]
	rm -f *$$py.class
	# Installer logs
	rm -f pip-log.txt
	rm -f pip-delete-this-directory.txt
	# Unit test / coverage reports
	rm -fr htmlcov/
	rm -fr .tox/
	rm -f .coverage
	rm -f .coverage.*
	rm -f .cache
	rm -f nosetests.xml
	rm -f coverage.xml
	rm -f *,cover
	rm -f .hypothesis/

# l l
