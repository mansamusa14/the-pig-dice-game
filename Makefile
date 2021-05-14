
#!/usr/bin/env make

# Change this to be your variant of the python command
#PYTHON = python3
PYTHON = python
#PYTHON = py

.PHONY: pydoc

all:


venv:
	[ -d .venv ] || $(PYTHON) -m venv .venv
	@printf "Now activate the Python virtual environment.\n"
	@printf "On Unix and Mac, do:\n"
	@printf ". .venv/bin/activate\n"
	@printf "On Windows (bash terminal), do:\n"
	@printf ". .venv/Scripts/activate\n"
	@printf "Type 'deactivate' to deactivate.\n"


install:
	$(PYTHON) -m pip install -r requirements.txt

installed:
	$(PYTHON) -m pip list

clean:
	rm -f .coverage *.pyc
	rm -rf __pycache__
	rm -rf htmlcov

clean-doc:
	rm -rf doc

clean-all: clean clean-doc
	rm -rf .venv

unittest:
	$(PYTHON) -m unittest discover . "*_test.py"


coverage:
	coverage run -m unittest discover . "*_test.py"
	coverage html
	coverage report -m

pylint:
	pylint *.py

flake8:
	flake8

pydoc:
	install -d doc/pydoc
	$(PYTHON) -m pydoc -w "$(PWD)"
	mv *.html doc/pydoc


pdoc:
	rm -rf doc/api
	pdoc --html -o doc/api .

doc: pdoc pyreverse #pydoc sphinx

pyreverse:
	install -d doc/uml
	pyreverse *.py
	dot -Tpng classes.dot -o doc/uml/classes.png
	dot -Tpng packages.dot -o doc/uml/packages.png
	rm -f classes.dot packages.dot
	ls -l doc/uml

radon-cc:
	radon cc . -a

radon-mi:
	radon mi .

radon-raw:
	radon raw .

radon-hal:
	radon hal .
