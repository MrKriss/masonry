
from pathlib import Path
import pytest
import git
import json
import os

from conftest import TEST_DIR
from masonry.objects.project import Project

from cookiecutter.exceptions import FailedHookException, UndefinedVariableInTemplate


@pytest.fixture(scope='module')
def init_simple_project(tmpdir_factory):

    temp_output_path = Path(tmpdir_factory.mktemp('simple_project').strpath)
    template_path = TEST_DIR / 'example_templates' / 'breaking_project1'

    # Set arguments
    init_variables = {
        "project_name": "new-project",
        "file1_text": "Hello World!"
    }

    project = Project(template_path)
    project.initialise(output_dir=temp_output_path, variables=init_variables)

    return project


@pytest.mark.parametrize(
    'layer', ('breaking_pre_hook', 'breaking_post_hook')
)
def test_rollback_when_error_in_pre_hook(init_simple_project, layer):

    # GIVEN an initialised project
    project = init_simple_project

    # WHEN adding a template that has a failing prehook
    with pytest.raises(FailedHookException):
        project.add_template(name=layer, variables={})

    # THEN only the original files should be present
    target = set([
        project.location / 'file_from_layer_1.txt',
        project.location / '.mason',
        # project.location / '.git',
    ])
    result = set(project.location.iterdir())
    assert result == target

    # THEN original file should be unchanged
    target = '123456'
    result_file = project.location / 'file_from_layer_1.txt'
    result = result_file.read_text()
    assert result == target


def test_rollback_when_error_in_variable_name(init_simple_project):

    # GIVEN an initialised project
    project = init_simple_project

    # WHEN a template is added that causes an error
    with pytest.raises(UndefinedVariableInTemplate):
        project.add_template(name='breaking_variable_name', variables={})

    # THEN only the original files should be present
    target = set([
        project.location / 'file_from_layer_1.txt',
        project.location / '.mason',
        # project.location / '.git',
    ])
    result = set(project.location.iterdir())
    assert result == target

    # THEN original file should be unchanged
    target = '123456'
    result_file = project.location / 'file_from_layer_1.txt'
    result = result_file.read_text()
    assert result == target


def test_rollback_when_init_project(tmpdir_factory):

    # GIVEN a temp directory and template to initialise
    temp_output_path = Path(tmpdir_factory.mktemp('empty_project').strpath)
    template_path = TEST_DIR / 'example_templates' / 'breaking_project2'

    init_variables = {
        "project_name": "new-project",
    }
    project = Project(template_path)

    # WHEN a new project is initialised that causes an error
    with pytest.raises(UndefinedVariableInTemplate):
        project.initialise(temp_output_path, variables=init_variables)

    # THEN the directory should be empty
    target = set([])
    result = set(temp_output_path.iterdir())
    assert result == target
