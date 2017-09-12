
.PHONY:load save remove

# Save new snapshot of environment 
freeze: 
	conda env export -n stone-mason -f package/frozen_environment.yml

# Load/update env based on environment file
load: 
	conda env update -n stone-mason -f package/dev_environment.yml

# Uninstall environment 
remove: 
	conda env remove -n stone-mason -f package/dev_environment.yml

.PHONY:test
# Run tests with Pytest 
test: 
	pytest --verbose --cov-report term --cov=stonemason package/tests --ignore package/tests/data

.PHONY:debug
# Run tests with Pytest with debug on 
debug: 
	pytest --verbose -s --pudb --cov-report term --cov=stonemason package/tests --ignore package/tests/data
