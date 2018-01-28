
# import attr

# @attr.s
# class Project:

#     filepath = attr.ib()

from pathlib import Path
import os
import json

from .template import Template

from ..resolution import create_dependency_graph, resolve
from ..prompt import prompt_cookiecutter_variables


class Project:

    def __init__(self, filepath, masonry_config=None, interactive=False):

        self.template_directory = Path(filepath).resolve()
        self.remaining_templates = [
            p.name for p in self.template_directory.iterdir() if p.is_dir()
        ]
        self.applied_templates = []

        self.template_variables = {}

        self.location = None

        self.interactive = interactive

        self.metadata_path = self.template_directory / 'metadata.json'
        self.metadata = json.load(open(self.metadata_path))

        if masonry_config is None:
            self.masonry_config = {}
        else:
            self.masonry_config = masonry_config

    def initialise(self, output_dir, variables):

        default_template_name = self.metadata['default']
        default_template_path = self.template_directory / default_template_name
        default_template = Template(default_template_path, variables)

        result = default_template.render(output_dir)

        self.location = Path(result).parent
        self.template_variables.update(variables)

        self._update_templates_remaining(default_template_name)

    def add_template(self, name, variables):

        self._check_all_variables_are_new(variables)
        variables.update(self.template_variables)

        template_path = self.template_directory / name
        template = Template(template_path, variables)

        template.render(output_dir=self.location)

        self._update_templates_remaining(name)

    def _update_templates_remaining(self, new_template_name):

        idx = self.remaining_templates.index(new_template_name)
        del self.remaining_templates[idx]
        self.applied_templates.append(new_template_name)

    def _check_all_variables_are_new(self, variables):

        current_variables = self.template_variables.keys()
        unique_keys = (
            key not in current_variables for key in variables.keys()
        )
        no_key_overlap = all(unique_keys)
        assert no_key_overlap

    #     # create it ------------------------

    #     # Work out all template names
    #     template_paths = {p.name: p for p in self.template_directory.iterdir() if p.is_dir()}
    #     template_names = list(template_paths.keys())

    #     # Create graph of template dependencies
    #     g = create_dependency_graph(self.metadata_path, node_list=template_names)

    #     # Resolve dependencies for specified template
    #     template_order = [n.name for n in resolve(g[template])]

    #     # Cycle through templates and render them
    #     for name in template_order:
    #         template = template_paths[name].as_posix()
    #         if self.interactive:
    #             context_variables = prompt_cookiecutter_variables(template, self.template_variables)
    #         else:
    #             context_variables_path = Path(template) / "cookiecutter.json"
    #             context_variables = json.load(context_variables_path.open())

    #     output_project_dir, content = safe_render(
    #         template, output_dir, context=context_variables)

    #     # This combines any prefix/postfix files added by the template to the originally named file
    #     # e.g. the cntent of 'Makefile_postfix' with be added to the end of the file 'Makefile',
    #     # and the cntent of 'MANIFEST_pretfix.in' with be added to the start of the file 'MANIFEST.in'
    #     combine_file_snippets(output_project_dir)

#         if not (Path(output_project_dir) / '.git').exists() and 'repo' not in vars():
#             # Initialise git repo
#             repo = git.Repo.init(output_project_dir)
#         else:
#             repo = git.Repo(output_project_dir)

#         # Save state
#         project_state['variables'].update(content)
#         if name not in project_state['templates']:
#             project_state['templates'].append(name)
#         project_state['project'] = project_path.name

#         # Save state of project variables
#         mason_vars = Path(output_project_dir) / '.mason'
#         with mason_vars.open('w') as f:
#             json.dump(project_state, f, indent=4)

#         # Commit template layer to git repo
#         all_files = [p.as_posix() for p in Path(output_project_dir).iterdir() if p.is_file]
#         repo.index.add(all_files)
#         repo.index.commit(f"Add '{name}' template layer via stone mason.")

#     return output_project_dir

#         return None


# def safe_render(template, target_dir, context, stream=STDOUT):
#     """Safely Render a new template by first making a backup to roll back to if needed."""

#     # Copy current directory to temp backup location
#     backup_dir = Path(tempfile.mkdtemp()) / 'backup'
#     backup = shutil.copytree(target_dir, backup_dir)

#     try:
#         output_dir, content = render_cookiecutter(
#             template, no_input=True,
#             extra_context=context,
#             output_dir=target_dir,
#             overwrite_if_exists=True,
#         )
#     except Exception as e:
#         # Rollback
#         puts(colored.red("An error occured during templating, Rolling back to last stable state."), stream=stream)
#         shutil.rmtree(target_dir)
#         shutil.copytree(backup, target_dir)
#         with indent(4):
#             puts(f'Restored {backup_dir} to {target_dir}', stream=stream)
#             puts(colored.red(f"Traceback: \n{e}"), stream=stream)
#         raise e
#         sys.exit()

#     # shutil.rmtree(backup_dir.as_posix())

#     return output_dir, content
