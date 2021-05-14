
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
