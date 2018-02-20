import json

import inquirer
from pathlib import Path

from .cli import CLI
from .project import Project


class App:

    def __init__(self, args, config=None):

        if not config:
            self.config = {
                "application_data": "~/.masonry/",
                "known_projects": {}
            }
        else:
            self.config = config

        app_data_dir = Path(self.config['application_data']).expanduser().resolve()
        if not app_data_dir.exists():
            app_data_dir.mkdir()

        self.app_data_dir = app_data_dir

        self.cli = CLI(args)
        self.args = self.cli._validate_args()

    def run(self):

        if self.args['init']:
            self.init_command()

        elif self.args['add']:
            self.add_command()

    def init_command(self, default_project=None):

        if not self.args['PROJECT']:
            self.args['PROJECT'] = self._prompt_init_project(default_project)

        project = Project(template_dir=self.args['PROJECT'])
        project.initialise(output_dir=self.args['--output'], variables={})
        self.project = project

        self._update_known_projects(project)

    def add_command(self, default_template=None):

        project_dir = Path(self.args['--output']).resolve()
        mason_file = project_dir / '.mason'

        if not mason_file.exists():
            raise IOError(
                f'A ".mason" file was not detected in the output directoty {project_dir}')

        project = Project(mason_file=mason_file)

        if not self.args['TEMPLATE']:
            # inquire which template to use
            self.args['TEMPLATE'] = self._prompt_add_template(project, default_template)

        for template_name in self.args['TEMPLATE']:
            project.add_template(template_name, variables={})

        self.project = project

    def _prompt_init_project(self, default=None):
        """Return the choice of project to intialise"""

        known_projects = list(self.config['known_projects'].keys())
        known_projects.sort()

        if not known_projects:
            raise ValueError("No project specified and no recent projects to choose from.")

        if default:
            default_idx = known_projects.index(default)
        else:
            default_idx = 0

        questions = [
            inquirer.List('project',
                          message="What project do you want to initialise?",
                          choices=known_projects,
                          default=default_idx)
        ]
        answers = inquirer.prompt(questions)

        project_path = known_projects[answers['project']]

        return project_path

    def _prompt_add_template(self, project, default=None):
        """Return the choice of templates to add"""

        remaining_templates_names = project.remaining_templates

        if default:
            default_idx = remaining_templates_names.index(default)
        else:
            default_idx = 0

        questions = [
            inquirer.Checkbox('templates',
                              message="What templates do you wish to add?",
                              choices=remaining_templates_names,
                              default=default_idx)
        ]

        answers = inquirer.prompt(questions)

        template_name = remaining_templates_names[answers['templates']]

        return template_name

    def _update_known_projects(self, project):

        project_name = project.template_directory.parent.name
        self.config['known_projects'][project_name] = str(project.template_directory)

        # Write to output
        known_projects_path = self.app_data_dir / 'known_projects.json'

        with known_projects_path.open('w', encoding='utf-8') as f:
            data = json.dump(self.config['known_projects'], f)
