
from pathlib import Path
import json

from .resolution import create_dependency_graph, resolve
from .render import render_cookiecutter


def initialise_project(project, template=None, output_dir='.'):

    project_path = Path(project)

    if not template:
        # Load metadata for project and read in default template from there
        meta_data_path = project_path / 'metadata.json'
        with meta_data_path.open() as meta_data_file:
            meta_data = json.load(meta_data_file)
        template = meta_data['default']

    # Work out all template names
    template_paths = {p.name: p for p in project_path.iterdir() if p.is_dir()}
    template_names = list(template_paths.keys())

    # Create graph of template dependencies
    g = create_dependency_graph(project_path / 'metadata.json',
                                node_list=template_names)

    # Resolve dependencies for specified template
    template_order = [n.name for n in resolve(g[template])]
    print(f'Creating project from templates:\n\t{template_order}')

    # Initialise output structure to save state of project
    project_state = {}
    project_state['templates'] = []
    project_state['variables'] = {}

    # Cycle through templates and render them
    for name in template_order:
        template = template_paths[name].as_posix()
        project_dir, content = render_cookiecutter(
            template,
            extra_context=project_state['variables'],
            output_dir=output_dir, overwrite_if_exists=True,
        )

        print(f'Rendered: {template}')

        # Save state
        project_state['variables'].update(content)
        project_state['templates'].append(name)

    # Save state of project variables
    mason_vars = Path(project_dir) / '.mason.json'
    with mason_vars.open('w') as f:
        json.dump(project_state, f)


def add_template(template, project_dir, output_dir='.'):
    """ Add a template to an existing project """

    # Load existing state information
    mason_vars = Path(project_dir) / '.mason.json'
    with mason_vars.open('r') as f:
        project_state = json.load(f)

    project_templates_root = Path(project_state['variables']['_template']).parent

    previous_templates = project_state['templates']

    paths = project_templates_root.iterdir()

    remaining_templates_paths = {
        p.name: p for p in paths if p.is_dir() and p.name not in previous_templates
    }

    assert template in remaining_templates_paths

    # Work out all template names
    remaining_templates_names = list(remaining_templates_paths.keys())

    # Create graph of template dependencies
    g = create_dependency_graph(project_templates_root / 'metadata.json',
                                node_list=remaining_templates_names)

    print(g)

    # Resolve dependencies for specified template
    template_order = [n.name for n in resolve(g[template])]
    print(f'Adding the following templates to project:\n\t{template_order}')

    # Cycle through templates and render them
    for name in template_order:
        template = remaining_templates_paths[name].as_posix()
        project_dir, content = render_cookiecutter(
            template,
            extra_context=project_state['variables'],
            output_dir=project_dir, overwrite_if_exists=True,
        )

        print(f'Rendered: {template}')

        # Save state
        project_state['variables'].update(content)
        project_state['templates'].append(name)

    # Save state of project variables
    with mason_vars.open('w') as f:
        json.dump(project_state, f)
