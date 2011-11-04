ALL:
.PHONY: tests tests-coverate

# Run unit tests.
# Requires Python 3.2
tests:
	python -m unittest discover -s tests -p '*.py'

# Run unit tests and collect coverage information in htmlcov/ directory.
# Note: coverage report won't include modules that weren't even imported!
# Required Python 3.2 and coverage.py
tests-coverage:
	-rm -r htmlcov
	coverage run -m unittest discover -s tests -p '*.py'
	coverage html
	echo 'Open htmlcov/index.html in your favourite browser'
