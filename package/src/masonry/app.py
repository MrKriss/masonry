import json
from pathlib import Path

import inquirer

from .cli import CLI
from .project import Project
from .utils import setup_logger
import py


class App:

    def __init__(self, args, config=None):

        self.cli = CLI(args)
        self.args = self.cli._validate_args()

        if self.args['-v']:
            self.logger = setup_logger(logfile=None, level='DEBUG')
        else:
            self.logger = setup_logger(logfile=None, level='INFO')

        self.logger.debug(f'Passed Arguments: {args}')

        if not config:
            self.config = {
                "application_data": "~/.masonry/",
                "known_projects": {}
            }
            self.logger.info(f'Using default config: {self.config}')

        else:
            self.config = config

        self.app_data_dir = Path(self.config['application_data']).expanduser().resolve()
        if not self.app_data_dir.exists():
            self.app_data_dir.mkdir()
            self.logger.info(f'Created Application directory: {self.app_data_dir}')

    def run(self):

        if self.args['init']:
            self.logger.debug(f'Started init command')
            self.init_command()
            self.logger.debug(f'Finished init command')

        elif self.args['add']:
            self.logger.debug(f'Started add command')
            self.add_command()
            self.logger.debug(f'Finished add command')

        elif self.args['check']:
            self.logger.debug(f'Started check command')
            self.check_command()
            self.logger.debug(f'Finished check command')

    def init_command(self, default_project=None):

        if not self.args['PROJECT']:
            self.args['PROJECT'] = self._prompt_init_project(default_project)

        project = Project(template_dir=self.args['PROJECT'])

        variables = self._prompt_cookiecutter_variables(
            project=project,
            template_name=project.metadata['default']
        )
        self.logger.info(f'Template Variables: {variables}')

        project.initialise(output_dir=self.args['--output'], variables=variables)
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

            variables = self._prompt_cookiecutter_variables(
                project=project,
                template_name=template_name
            )
            project.add_template(template_name, variables=variables)

        self.project = project

    def check_command(self, default_project=None):

        if not self.args['PROJECT']:
            self.args['PROJECT'] = self._prompt_init_project(default_project)

        project = Project(template_dir=self.args['PROJECT'])

        default_template = project.metadata['default']

        template_orders = {}
        for layer in project.remaining_templates:
            if layer != default_template:
                dependencies = project._g.get_dependencies(layer)
                dependencies = [x for x in dependencies if x != default_template]
                template_orders[layer] = dependencies

        tmpdir = py.path.local.mkdtemp().mkdir('check')
        self.check_dir = tmpdir

        error_log = []

        for layer, deps in template_orders.items():

            project = Project(template_dir=self.args['PROJECT'])

            output_dir = tmpdir.mkdir(layer)
            print(f'Testing Layer: {layer}')
            print(f'Installing: {deps}')

            project.initialise(output_dir=output_dir, variables={})

            for dep in deps:
                try:
                    print(f'Adding layer: {dep}')
                    project.add_template(name=dep, variables={})
                except Exception as e:
                    msg = f'{e} encountered on adding "{dep}" to project for layer "{layer}"'
                    error_log.append(msg)

        if error_log:
            print("Errors were encountered:")
            for err in error_log:
                print(err)
        else:
            print("All template layers created without error")

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

    def _prompt_cookiecutter_variables(self, project, template_name):

        cookiecutter_vars_path = project.template_directory / template_name / "cookiecutter.json"

        with cookiecutter_vars_path.open() as f:
            cookiecutter_vars = json.load(f)

        # Construct list of questions for variables without a value
        questions = []
        for key, value in cookiecutter_vars.items():

            if key not in project.template_variables:

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

    def _update_known_projects(self, project):

        self.logger.debug(f'Previous Known Projects: {self.config["known_projects"]}')

        project_name = project.template_directory.parent.name
        self.config['known_projects'][project_name] = str(project.template_directory)

        self.logger.debug(f'Updated Known Projects: {self.config["known_projects"]}')

        # Write to output
        known_projects_path = self.app_data_dir / 'known_projects.json'

        with known_projects_path.open('w', encoding='utf-8') as f:
            json.dump(self.config['known_projects'], f)
