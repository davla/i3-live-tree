# This makefile defines tasks for the project that aren't already defined by
# poetry. It serves more or less the purpose of npm package.json's "scripts"
# section

EXEC := poetry run

test:
	$(EXEC) python -m unittest -v -b
