ALL:
.PHONY: tests

# Run unit tests (requires Python 3.2)
tests:
	python -m unittest discover -s tests -p '*.py'
