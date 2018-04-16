targets = \
  help

target_help = \
  'help - Prints this help message.' \
  ' ' \
  'code-check - Runs pycodestyle on all files in the repo'


help:
	@echo "Valid targets are:\n"
	@for t in $(target_help) ; do \
	    echo $$t; done
	@echo


code-check:
	@pycodestyle *.py */*.py
	@flake8 *.py */*.py
