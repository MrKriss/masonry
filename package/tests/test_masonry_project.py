
import pytest
from masonry.objects.project import Project
from pathlib import Path
import py.path


@pytest.fixture
def project_templates_path():
    return (
        py.path.local(__file__)
        .dirpath()
        .join('example_templates/simple_project')
    )


def test_can_create_project_with_all_attributes(project_templates_path, tmpdir):

    masonry_config = {
        'other-project': 'some/path/to/it'
    }

    project = Project(project_templates_path, masonry_config=masonry_config)

    assert project.template_directory == Path(project_templates_path)
    assert set(project.remaining_templates) == set(['first_layer', 'second_layer', 'third_layer'])
    assert project.applied_templates == []
    assert project.template_variables == {}

    assert project.metadata_path == Path(project_templates_path) / 'metadata.json'
    target = {
        "default": "first_layer",
        "dependencies": {
            "second_layer": [
                "first_layer"
            ],
            "third_layer": [
                "second_layer"
            ]
        }
    }
    assert project.metadata == target
    assert project.masonry_config == masonry_config


@pytest.mark.xfail
def test_can_create_project(project_templates_path, tmpdir):

    project = Project(project_templates_path)

    variables = {
        "project_name": "new-project",
        "file1_text": "Hello World!"
    }

    project.initialise(output_path=tmpdir.strpath, variables=variables)

    project_path = tmpdir.join(variables['project_name'])

    assert project_path.check(dir=True)
