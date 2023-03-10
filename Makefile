PYTHON=python
TWINE=twine

test:
	${PYTHON} -m unittest discover gc_google_services_api/ "test_*.py"

lint:
	flake8

lint-fix:
	isort .

version:
	poetry version $(version)
	git commit -am "Release $(version)"
	git tag $(version)
	git push --follow-tags