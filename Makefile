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

test:
	@pytest


coverage: coverage-run coverage-report coverage-html-report

coverage-run:
	@py.test --no-cov

coverage-report: diff_files:=$(shell git diff --name-only $(branch))
coverage-report: diff_sed:=$(shell echo $(diff_files)| sed s:web/impact/::g)
coverage-report: diff_grep:=$(shell echo $(diff_sed) | tr ' ' '\n' | grep \.py | grep -v /tests/ | grep -v /django_migrations/ | tr '\n' ' ' )
coverage-report:
	@coverage report -i --skip-covered $(diff_grep) | grep -v "NoSource:"

coverage-html-report:
	@coverage html --omit="*/tests/*"

