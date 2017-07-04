import inquirer

from pathlib import Path


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
        p.name: p for p in paths if p.is_dir() and p.name not in previous_templates
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

    print(answers)

    templates = answers['templates']

    return templates
