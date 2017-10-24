
import json

import pytest

from masonry.resolution import create_dependency_graph, resolve
import py.path
from masonry.template import initialise_project, add_template


TEMPLATE_COLLECTION_PATH = py.path.local(__file__).dirpath()


@pytest.fixture(autouse=True)
def no_prompts(monkeypatch):

    import inquirer

    def mock_inquirer_prompt(questions):
        answers = {q.name: q.default for q in questions}
        return answers

    # Mock the interactive input and use cookiecutter defaults instead
    monkeypatch.setattr(inquirer, 'prompt', mock_inquirer_prompt)


@pytest.fixture
def template_orders():

    metadata = TEMPLATE_COLLECTION_PATH.join('metadata.json')
    layers = [x.basename for x in TEMPLATE_COLLECTION_PATH.listdir()
              if x.isdir() and x.basename != '__pycache__']

    g = create_dependency_graph(metadata, layers)

    orders = {}
    for layer in layers:
        orders[layer] = [x.name for x in resolve(g[layer])]

    return orders


@pytest.fixture
def default_template():

    # Find default template
    metadata = json.load(TEMPLATE_COLLECTION_PATH.join('metadata.json'))
    default_template = metadata['default']

    return default_template


def test_all_layers(template_orders, default_template, tmpdir):

    # Given the order of all dependencies for the template layers
    if default_template in template_orders:
        del template_orders[default_template]

    # When adding each in turn
    for layer, deps in template_orders.items():

        if default_template in deps:
            deps.remove(default_template)

        output_dir = tmpdir.mkdir(layer)
        print('Testing Layer:', layer)
        print('Initialising with default template')
        project_dir = initialise_project(TEMPLATE_COLLECTION_PATH, output_dir=str(output_dir))

        for dep in deps:
            print('Adding layer:', dep)
            add_template([dep], project_dir)


# def test_bake_all_template_layers(cookies, template_orders):
#     """Test for 'cookiecutter-template'."""

#     for idx, (layer, deps) in enumerate(template_orders.items()):
#         cookies._count = idx
#         for dep in deps:
#             result = cookies.bake(template=str(dep))
#             cookies._count = idx

#             assert result.exit_code == 0
#             assert result.exception is None
