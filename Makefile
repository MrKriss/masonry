
.PHONY:load save remove

# Save new snapshot of environment 
refreeze: 
	conda env create -n testenv -f package/dev_environment.yml	
	conda env export -n testenv -f package/frozen_environment.yml
	conda env remove -n testenv

# Load/update env based on latest version of libraries in dev_environment file
update: 
	conda env update -n stone-mason -f package/dev_environment.yml

# Reset env based on frozen version of libraries in frozen_environment file
rollback:
	conda env update -n stone-mason -f package/frozen_environment.yml

.PHONY:test
# Run tests with Pytest 
test: 
	pytest --verbose --cov-report term --cov=stonemason package/tests --ignore package/tests/data

.PHONY:debug
# Run tests with Pytest with debug on 
debug: 
	pytest --verbose -s --pudb --cov-report term --cov=stonemason package/tests --ignore package/tests/data
