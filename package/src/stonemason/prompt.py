import inquirer

from pathlib import Path
import json

IGNORED_DIRS = [
    '__pycache__',
    '.git'
]


def prompt_init_project(project_templates):
    """Return the choice of project to intialise"""

    projects = list(project_templates.keys())
    projects.sort()

    questions = [
        inquirer.List('project',
                      message="What project do you want to initialise?",
                      choices=projects)
    ]

    answers = inquirer.prompt(questions)

    project_path = project_templates[answers['project']]

    return project_path


def prompt_add_template(project_template_root, project_state):
    """Return the choice of templates to add"""

    project_template_root = Path(project_template_root).resolve()

    # Find remaining templates that can be applied
    previous_templates = project_state['templates']

    paths = project_template_root.iterdir()

    remaining_template_paths = {
        p.name: p for p in paths
        if p.is_dir() and p.name not in previous_templates and p.name not in IGNORED_DIRS
    }

    print(remaining_template_paths.keys())

    remaining_templates_names = list(remaining_template_paths.keys())
    remaining_templates_names.sort()

    questions = [
        inquirer.Checkbox('templates',
                          message="What templates do you wish to add?",
                          choices=remaining_templates_names)
    ]

    answers = inquirer.prompt(questions)

    templates = answers['templates']

    return templates


def prompt_cookiecutter_variables(template, context_variables):

    template_path = Path(template)
    cookiecutter_vars_path = template_path / "cookiecutter.json"

    with cookiecutter_vars_path.open() as f:
        cookiecutter_vars = json.load(f)

    current_variables = list(context_variables.keys())

    # Construct list of questions for variables without a value
    questions = []
    for key, value in cookiecutter_vars.items():

        if key not in current_variables:

            var_name = key.replace("_", " ").title()

            if isinstance(value, (str, int, float, bool)):
                questions.append(
                    inquirer.Text(key,
                                  message=f"Please specify '{var_name}'",
                                  default=value)
                )
            elif isinstance(value, list):
                questions.append(
                    inquirer.List(key,
                                  message=f"Please specify '{var_name}'",
                                  default=value[0],
                                  choices=value)
                )

    answers = inquirer.prompt(questions)

    return answers
