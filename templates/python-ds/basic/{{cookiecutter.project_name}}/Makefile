
.PHONY:refreeze update rolback

# Save new snapshot of environment 
refreeze: 
	conda env create -n testenv -f dev_environment.yml	
	conda env export -n testenv -f frozen_environment.yml
	conda env remove -n testenv

# Load/update env based on latest version of libraries in dev_environment file
update: 
	conda env update -n {{cookiecutter.project_name}} -f dev_environment.yml

# Reset env based on frozen version of libraries in frozen_environment file
rollback:
	conda env update -n {{cookiecutter.project_name}} -f frozen_environment.yml
