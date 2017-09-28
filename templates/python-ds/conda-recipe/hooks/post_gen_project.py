""" Hook to add all items in the dev_environment file to the conda meat.ymal run requirements """

import re
import textwrap
from pathlib import Path

from ruamel.yaml import YAML

PY_VERSON = "python={{cookiecutter.python_version}}"

# Define Paths
environment_file = Path('.').resolve() / 'package' / 'dev_environment.yml'
conda_metadata_file = (
    Path('.').resolve() / 'package' / 'recipes' /
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


# Comment out dependencies in the setup.py file

def comment_out_setup_dependencies(setup_file_path):

    setup_file_path = Path(setup_file_path)
    pattern = re.compile(r" *install_requires\s*=\s*\[.*?\]", flags=re.DOTALL)

    # Match the install_requires section
    res = pattern.search(setup_file_path.read_text())

    # Extract the matched substring and comment out every line
    new_string = res.group()
    new_string = textwrap.dedent(new_string)
    new_string = textwrap.indent(new_string, prefix='# ')
    new_string = textwrap.indent(new_string, prefix='    ')

    # Substitute new substring into position in the file
    new_text = pattern.sub(new_string, res.string)
    setup_file_path.write_text(new_text)


comment_out_setup_dependencies('package/setup.py')
