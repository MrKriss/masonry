import json
import os
from pathlib import Path

import git

from .postprocessors import CombineFilePostfix, CombineFilePrefix
from .resolution import DependencyGraph
from .template import Template


class Project:

    def __init__(self, template_dir=None, mason_file=None, masonry_config=None,
                 interactive=False, use_git=False):

        if template_dir:
            self.template_directory = Path(template_dir).resolve()
            self.remaining_templates = [
                p.name for p in self.template_directory.iterdir() if p.is_dir()
            ]
            self.applied_templates = []
            self.template_variables = {}
            self.location = None
            self.parent_dir = None

        elif mason_file:
            mason_file = Path(mason_file)
            mason_data = json.load(open(mason_file))
            self.template_directory = Path(mason_data['template_directory'])
            self.remaining_templates = mason_data['remaining_templates']
            self.applied_templates = mason_data['applied_templates']
            self.template_variables = mason_data['template_variables']
            self.location = Path(mason_data['project_location'])
            self.parent_dir = self.location.parent

        self.interactive = interactive
        self.use_git = use_git

        self._postprocessors = [
            CombineFilePrefix(),
            CombineFilePostfix()
        ]

        self.metadata_path = self.template_directory / 'metadata.json'
        self.metadata = json.load(open(self.metadata_path))

        # Create graph of template dependencies
        self._g = DependencyGraph(
            self.metadata,
            template_list=self.remaining_templates
        )

        if masonry_config is None:
            self.masonry_config = {
                'replay_dir': Path('~/.cookiecutter_replay/').expanduser().resolve()
            }
        else:
            self.masonry_config = masonry_config

    def initialise(self, output_dir, variables):

        default_template_name = self.metadata['default']
        output_dir, variables = self.render_template(
            name=default_template_name,
            variables=variables,
            output_dir=output_dir
        )

        self.location = Path(output_dir)
        self.parent_dir = Path(output_dir).parent
        self._update_and_save_state(default_template_name, variables)

    def add_template(self, name, variables):

        # Find all template dependencies
        templates_to_apply = self._g.get_dependencies(name)

        # Render each template in turn
        for template in templates_to_apply:
            if template in self.applied_templates:
                continue
            output_dir, variables = self.render_template(template, variables)
            self._apply_postprocessing()
            self._update_and_save_state(template, variables)

    def render_template(self, name, variables, output_dir=None):

        if not output_dir:
            output_dir = self.parent_dir

        template_path = self.template_directory / name
        variables.update(self.template_variables)

        template = Template(template_path, variables)
        output_path = template.render(output_dir=output_dir)

        # Get rendered variables from replay contest
        replay_file = self.masonry_config['replay_dir'] / f'{name}.json'
        context = json.load(replay_file.open(encoding='utf-8'))
        del context['cookiecutter']['_template']

        return output_path, context['cookiecutter']

    def _apply_postprocessing(self):

        for dirpath, dirnames, filenames in os.walk(self.location):

            if '.git' in dirnames:
                dirnames.remove('.git')

            if filenames:
                for p in self._postprocessors:
                    p.apply(dirpath)

    def _update_and_save_state(self, template_name, variables):
        self.template_variables.update(variables)
        self._update_templates_remaining(template_name)
        self._save_state_to_mason_file()
        self._commit_to_git(template_name)

    def _update_templates_remaining(self, applied_template):

        idx = self.remaining_templates.index(applied_template)
        del self.remaining_templates[idx]
        self.applied_templates.append(applied_template)

    def _save_state_to_mason_file(self):

        mason_data = dict(
            applied_templates=self.applied_templates,
            remaining_templates=self.remaining_templates,
            template_directory=self.template_directory.as_posix(),
            template_variables=self.template_variables,
            project_location=self.location.as_posix()
        )
        mason_file_path = self.location / '.mason'
        with mason_file_path.open('w', encoding='utf-8') as f:
            json.dump(mason_data, f)

    def _commit_to_git(self, template_name):

        if not self.use_git:
            return None

        git_dir = self.location / '.git'

        if not git_dir.exists():
            # Initialise git repo
            repo = git.Repo.init(self.location)
        else:
            repo = git.Repo(self.location)

        # Commit template layer to git repo
        all_files = [p.as_posix() for p in self.location.iterdir() if p.is_file]
        repo.index.add(all_files)
        repo.index.commit(f"Add '{template_name}' template layer via masonry.")
