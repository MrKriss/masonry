""" Hook to add all items in the requirements file to the conda meat.ymal run requirements """

import pathlib
import yaml
import pip.req

requirements_file = pathlib.Path('.').resolve() / 'package' / 'requirements.txt'
conda_metadata_file = pathlib.Path('.').resolve() / 'package' / 'recipe' / 'meta.yaml'

if requirements_file.exists():
    dependencies = []
    
    for item in pip.req.parse_requirements(requirements_file.as_posix(), session="somesession"):
        if isinstance(item, pip.req.InstallRequirement):
            dep = f"{item.name} {item.req.specifier}"
            dependencies.append(dep)

    # Load existing conda metadata, append dependencies and write back out
    conda_recipe = yaml.load(conda_metadata_file.open())
    conda_recipe['requirements']['run'].extend(dependencies)
    yaml.dump(conda_recipe, conda_metadata_file.open(mode='w'), default_flow_style=False)
