PYTHON=python
TWINE=twine

test:
	poetry run ${PYTHON} -m unittest discover gc_google_services_api/ "test_*.py"

lint:
	flake8

lint-fix:
	isort .

release:
	poetry version $(v)
	git commit -am "Release $(v)"
	git tag $(v)
	git push --follow-tags