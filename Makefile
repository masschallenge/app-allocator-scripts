targets = \
  help

target_help = \
  'help - Prints this help message.' \
  ' ' \
  'code-check - Runs pycodestyle on all files in the repo' \
  'test - runs tests' \
  'coverage - runs tests and produces terminal and html reports'


VENV = venv
ACTIVATE_SCRIPT = $(VENV)/bin/activate
ACTIVATE = export PYTHONPATH=.; . $(ACTIVATE_SCRIPT)


help:
	@echo "Valid targets are:\n"
	@for t in $(target_help) ; do \
	    echo $$t; done
	@echo

code-check:
	@pycodestyle *.py */*.py
	@flake8 *.py */*.py

$(VENV): Makefile requirements.txt
	@pip install virtualenv
	@rm -rf $(VENV)
	@virtualenv -p `which python3` $@
	@touch $(ACTIVATE_SCRIPT)
	@$(ACTIVATE) ; \
	DJANGO_VERSION=$(DJANGO_VERSION) pip install -r requirements.txt

test: $(VENV)
	@$(ACTIVATE) ; pytest

coverage: $(VENV)
	@$(ACTIVATE) ; pytest --cov=app_allocator --cov-report=term --cov-report=html
