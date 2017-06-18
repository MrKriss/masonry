
.PHONY:load save remove

# Save new snapshot of environment 
save: 
	conda env export -n my-project -f environment.yml

# Load/update env based on environment file
load: 
	conda env update -n my-project -f environment.yml

# Uninstall environment 
remove: 
	conda env remove -n my-project -f environment.yml

.PHONY:test
# Run tests with Pytest 
test: 
	pytest --verbose --cov-report term --cov=mypackage package/tests