PYTHON=python
TWINE=twine

test:
	${PYTHON} -m unittest discover gc_google_services_api/ "test_*.py"

build:
	${PYTHON} setup.py bdist_wheel 

deploy:
	${TWINE} upload dist/* 