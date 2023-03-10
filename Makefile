PYTHON=python
TWINE=twine

test:
	${PYTHON} -m unittest discover gc_google_services_api/ "test_*.py"

lint:
	flake8

lint-fix:
	isort .

deploy:
	${PYTHON} setup.py bdist_wheel 
	${TWINE} upload dist/* 