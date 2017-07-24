
.PHONY:load save remove

# Save new snapshot of environment 
save: 
	conda env export -n stone-mason -f environment.yml

# Load/update env based on environment file
load: 
	conda env update -n stone-mason -f environment.yml

# Uninstall environment 
remove: 
	conda env remove -n stone-mason -f environment.yml

.PHONY:test
# Run tests with Pytest 
test: 
	pytest --verbose --cov-report term --cov=stonemason --ignore=package/tests/data/ package/tests/ 

.PHONY:debug
# Run tests with Pytest 
debug: 
	pytest --verbose -s --pudb --cov-report term --cov=stonemason --ignore=package/tests/data/ package/tests/ 