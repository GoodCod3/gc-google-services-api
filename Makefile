PYTHON=python

test:
	${PYTHON} -m unittest discover gc_google_services_api/ "test_*.py"