
import json

import py.path
import pytest

from masonry.resolution import create_dependency_graph, resolve
from masonry.template import initialise_project, add_template


TEMPLATE_COLLECTION_PATH = (
    py.path.local(__file__)
    .dirpath()
    .join('example_templates/python_project')
)


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
