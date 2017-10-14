
import json
import shutil
import sys
import tempfile
from pathlib import Path

import git
from clint.textui import colored, prompt, puts, validators

from .postprocess import combine_file_snippets
from .render import render_cookiecutter
from .resolution import create_dependency_graph, resolve
from .utils import load_application_data, save_application_data

from.prompt import prompt_cookiecutter_variables


def initialise_project(project: Path, template=None, output_dir='.'):

    # Initialise path variables
    project_path = Path(project).resolve()
    meta_data_path = project_path / 'metadata.json'
    project_templates = load_application_data()

    # If project is a valid project file
    if not meta_data_path.exists():
        raise IOError("Not a valid project directory. Missing metadata.json file")

    if not template:
        # Load metadata for project and read in default template from there
        with meta_data_path.open() as meta_data_file:
            meta_data = json.load(meta_data_file)
        template = meta_data['default']

    # Store location of project template
    if project_path.name in project_templates:
        if project_templates[project_path.name] != project_path.as_posix():
            ans = prompt.query(
                "Project with the same name already exists in another location. Overwrite? [y/n]",
                validators=[validators.RegexValidator('[yn]')])
            if ans == 'n':
                sys.exit()

    project_templates[project_path.name] = project_path.as_posix()
    save_application_data(project_templates)

    # Work out all template names
    template_paths = {p.name: p for p in project_path.iterdir() if p.is_dir()}
    template_names = list(template_paths.keys())

    # Create graph of template dependencies
    g = create_dependency_graph(project_path / 'metadata.json',
                                node_list=template_names)

    # Resolve dependencies for specified template
    template_order = [n.name for n in resolve(g[template])]
    puts(f'Creating project from templates:\n\t{template_order}')

    # Initialise output structure to save state of project
    project_state = {}
    project_state['templates'] = []
    project_state['variables'] = {}

    # Cycle through templates and render them
    for name in template_order:
        template = template_paths[name].as_posix()
        context_variables = prompt_cookiecutter_variables(template, project_state['variables'])

        output_project_dir, content = safe_render(
            template, output_dir, context=context_variables
        )

        # This combines any prefix/postfix files added by the template to the originally named file
        # e.g. the cntent of 'Makefile_postfix' with be added to the end of the file 'Makefile',
        # and the cntent of 'MANIFEST_pretfix.in' with be added to the start of the file 'MANIFEST.in'
        combine_file_snippets(output_project_dir)

        if not (Path(output_project_dir) / '.git').exists() and 'repo' not in vars():
            # Initialise git repo
            repo = git.Repo.init(output_project_dir)
        else:
            repo = git.Repo(output_project_dir)

        puts(f'Rendered: {template}')

        # Save state
        project_state['variables'].update(content)
        if name not in project_state['templates']:
            project_state['templates'].append(name)
        project_state['project'] = project_path.name

        # Save state of project variables
        mason_vars = Path(output_project_dir) / '.mason'
        with mason_vars.open('w') as f:
            json.dump(project_state, f, indent=4)

        # Commit template layer to git repo
        all_files = [p.as_posix() for p in Path(output_project_dir).iterdir() if p.is_file]
        repo.index.add(all_files)
        repo.index.commit(f"Add '{name}' template layer via stone mason.")

    return output_project_dir


def add_template(templates: list, project_dir: Path):
    """ Add a template to an existing project """

    project_dir = Path(project_dir).resolve()
    repo = git.Repo(project_dir.as_posix())

    # Load existing state information
    mason_vars = project_dir / '.mason'
    with mason_vars.open('r') as f:
        project_state = json.load(f)

    # Load project locations and get project root path
    project_template_data = load_application_data()
    project_root = Path(project_template_data[project_state['project']])

    # Find remaining templates that can be applied
    previous_templates = project_state['templates']
    paths = project_root.iterdir()
    template_paths = {p.name: p for p in paths if p.is_dir()}

    templates_names = list(template_paths.keys())
    templates_names.sort()

    for t in templates:
        assert t in templates_names, f'{t} not in templates for this type of project'

    # Create graph of template dependencies
    g = create_dependency_graph(project_root / 'metadata.json',
                                node_list=templates_names)

    # Resolve dependencies for specified template
    template_orders = []

    for t in templates:
        order = [n.name for n in resolve(g[t]) if n.name not in previous_templates]
        if order:
            template_orders.append(order)
            previous_templates.extend(order)

    puts(f'Adding the following templates to project:\n\t{template_orders}')

    # Cycle through templates and render them
    for order_set in template_orders:

        for name in order_set:
            template = template_paths[name].as_posix()
            context_variables = prompt_cookiecutter_variables(template, project_state['variables'])
            project_state['variables'].update(context_variables)

            output_project_dir, content = safe_render(
                template,
                target_dir=project_dir.parent,
                context=project_state['variables']
            )

            puts(f'Rendered: {template}')

            # This combines any prefix/postfix files added by the template to the originally named file
            # e.g. the cntent of 'Makefile_postfix' with be added to the end of the file 'Makefile',
            # and the cntent of 'MANIFEST_pretfix.in' with be added to the start of the file 'MANIFEST.in'
            combine_file_snippets(output_project_dir)

            # Save state
            project_state['variables'].update(content)
            if name not in project_state['templates']:
                project_state['templates'].append(name)

            # Save state of project variables
            with mason_vars.open('w') as f:
                json.dump(project_state, f, indent=4)

            output_project_dir = Path(output_project_dir)

            # Commit template layer to git repo
            repo.git.add(output_project_dir.as_posix(), force=False)
            repo.index.commit(f"Add '{name}' template layer via stone mason.")


def safe_render(template, target_dir, context):
    """Safely Render a new template by first making a backup to roll back to if needed."""

    # Copy current directory to temp backup location
    backup_dir = Path(tempfile.mkdtemp()) / 'backup'
    backup = shutil.copytree(target_dir, backup_dir)

    try:
        output_dir, content = render_cookiecutter(
            template, no_input=True,
            extra_context=context,
            output_dir=target_dir,
            overwrite_if_exists=True,
        )
    except Exception as e:
        # Rollback
        print("The following error occurs during templating, Rolling back to last stable state.")
        print(e)
        shutil.rmtree(target_dir)
        shutil.copytree(backup, target_dir)
        print(f'Copied {backup_dir} to {target_dir}')
        raise(e)

    shutil.rmtree(backup_dir.as_posix())

    return output_dir, content
