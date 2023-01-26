PYTHON=python
TWINE=twine

test:
	${PYTHON} -m unittest discover gc_google_services_api/ "test_*.py"

deploy:
	${PYTHON} setup.py bdist_wheel 
	${TWINE} upload dist/* 