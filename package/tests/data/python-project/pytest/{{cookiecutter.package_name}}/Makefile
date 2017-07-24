.PHONY:test
# Run tests with Pytest 
test: 
	pytest --verbose --cov-report term --cov={{cookiecutter.package_name}} tests/

.PHONY:debug
# Run tests with Pytest 
debug: 
	pytest --verbose -s --pudb --cov-report term --cov={cookiecutter.package_name}} tests/ 