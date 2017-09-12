""" Hook to add all items in the dev_environment file to the conda meat.ymal run requirements """

import pathlib
from ruamel.yaml import YAML

PY_VERSON = "python={{cookiecutter.python_version}}"

# Define Paths
environment_file = pathlib.Path('.').resolve() / 'package' / 'dev_environment.yml'
conda_metadata_file = (
    pathlib.Path('.').resolve() / 'package' / 'recipes' /
    '{{cookiecutter.package_name}}' / 'meta.yaml'
)

# init parser
yaml = YAML()
yaml.default_flow_style = False

# Read in files
environment_spec = yaml.load(environment_file.open())
conda_recipe = yaml.load(conda_metadata_file.open())

# Update
for package in environment_spec['dependencies']:
    if isinstance(package, str):
        if not package.startswith(PY_VERSON):
            conda_recipe['requirements']['run'].append(package)

# Write out
yaml.dump(conda_recipe, conda_metadata_file.open(mode='w'))
