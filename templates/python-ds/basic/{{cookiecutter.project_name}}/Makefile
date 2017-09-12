
.PHONY:load save remove

# Save new snapshot of environment 
freeze: 
	conda env export -n {{cookiecutter.project_name}} -f frozen_environment.yml

# Load/update env based on environment file
load: 
	conda env update -n {{cookiecutter.project_name}} -f dev_environment.yml

# Uninstall environment 
remove: 
	conda env remove -n {{cookiecutter.project_name}} -f dev_environment.yml

