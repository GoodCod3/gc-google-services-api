PYTHON=python
TWINE=twine

test:
	${PYTHON} -m unittest discover gc_google_services_api/ "test_*.py"

lint:
	flake8

lint-fix:
	isort .
