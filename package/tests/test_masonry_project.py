
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


def test_can_create_project_with_required_attributes(project_templates_path, tmpdir):

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


def test_can_create_project_with_default_template(project_templates_path, tmpdir):

    project = Project(template_dir=project_templates_path)

    variables = {
        "project_name": "new-project",
        "file1_text": "Hello World!"
    }

    project.initialise(output_dir=tmpdir.strpath, variables=variables)

    project_path = tmpdir.join(variables['project_name'])
    created_file = project_path.join('file_from_layer_1.txt')

    assert project_path.check(dir=True)
    assert created_file.check(file=True)
    content = created_file.read_text('utf8')
    assert variables['file1_text'] in content

    assert project.applied_templates == ['first_layer']
    assert 'first_layer' not in project.remaining_templates


def test_can_add_template_layer_after_default_template(project_templates_path, tmpdir):

    project = Project(template_dir=project_templates_path)

    init_variables = {
        "project_name": "new-project",
        "file1_text": "Hello World!"
    }

    project.initialise(output_dir=tmpdir.strpath, variables=init_variables)

    second_layer_variables = {
        "file2_text": "This text is a test"
    }

    project.add_template(name='second_layer', variables=second_layer_variables)

    project_path = tmpdir.join(init_variables['project_name'])
    created_file = project_path.join('file_from_layer_2.txt')

    assert project_path.check(dir=True)
    assert created_file.check(file=True)
    content = created_file.read_text('utf8')
    assert second_layer_variables['file2_text'] in content

    assert project.applied_templates == ['first_layer', 'second_layer']
    assert 'first_layer' not in project.remaining_templates
    assert 'second_layer' not in project.remaining_templates


def test_can_resolve_template_order_and_apply_them(project_templates_path, tmpdir):

    project = Project(template_dir=project_templates_path)

    init_variables = {
        "project_name": "new-project",
        "file1_text": "Hello World!"
    }

    project.initialise(output_dir=tmpdir.strpath, variables=init_variables)

    second_layer_variables = {
        "file2_text": "This text is a test",
        "Othernot needed": "variable"
    }

    project.add_template(name='third_layer', variables=second_layer_variables)

    project_path = tmpdir.join(init_variables['project_name'])
    created_file = project_path.join('file_from_layer_2.txt')

    assert project_path.check(dir=True)
    assert created_file.check(file=True)
    content = created_file.read_text('utf8')
    assert second_layer_variables['file2_text'] in content

    assert project.applied_templates == ['first_layer', 'second_layer', 'third_layer']
    assert project.remaining_templates == []


def test_can_perform_file_post_and_prefix_merging(project_templates_path, tmpdir):

    project = Project(template_dir=project_templates_path)

    init_variables = {
        "project_name": "new-project",
        "file1_text": "Hello World!"
    }

    project.initialise(output_dir=tmpdir.strpath, variables=init_variables)
    project.add_template(name='third_layer', variables={})

    project_path = tmpdir.join(init_variables['project_name'])
    assert project_path.check(dir=True)

    created_file1 = project_path.join('file_from_layer_1.txt')
    assert created_file1.check(file=True)
    content = created_file1.read_text('utf8')
    print(content)
    assert 'Prefixed text' in content

    created_file = project_path.join('file_from_layer_2.txt')
    assert created_file.check(file=True)
    content = created_file.read_text('utf8')
    print(content)
    assert 'Postfixed text' in content

    assert project.applied_templates == ['first_layer', 'second_layer', 'third_layer']
    assert project.remaining_templates == []


def test_can_recreate_project_from_mason_file_after_being_initialised(project_templates_path, tmpdir):

    project1 = Project(template_dir=project_templates_path)

    init_variables = {
        "project_name": "new-project",
        "file1_text": "Hello World!"
    }

    project1.initialise(output_dir=tmpdir.strpath, variables=init_variables)

    mason_file_path = Path(tmpdir) / init_variables['project_name'] / '.mason'
    project2 = Project(mason_file=mason_file_path)

    attributes = [k for k in project1.__dict__.keys() if not k.startswith('_')]
    for attr in attributes:
        assert project1.__dict__[attr] == project2.__dict__[attr]


def test_can_recreate_project_from_mason_file_after_first_layer(project_templates_path, tmpdir):

    project1 = Project(template_dir=project_templates_path)
    init_variables = {
        "project_name": "new-project",
        "file1_text": "Hello World!"
    }
    project1.initialise(output_dir=tmpdir.strpath, variables=init_variables)

    second_layer_variables = {
        "file2_text": "This text is a test",
    }
    project1.add_template(name='third_layer', variables=second_layer_variables)

    mason_file_path = Path(tmpdir) / init_variables['project_name'] / '.mason'
    project2 = Project(mason_file=mason_file_path)

    attributes = [k for k in project1.__dict__.keys() if not k.startswith('_')]
    for attr in attributes:
        assert project1.__dict__[attr] == project2.__dict__[attr]


@pytest.mark.xfail
def test_can_commit_template_layers_to_git_repo(project_templates_path, tmpdir):

    project = Project(template_dir=project_templates_path)

    init_variables = {
        "project_name": "new-project",
        "file1_text": "Hello World!"
    }
    project.initialise(output_dir=tmpdir.strpath, variables=init_variables)

    second_layer_variables = {
        "file2_text": "This text is a test",
    }
    project.add_template(name='third_layer', variables=second_layer_variables)

    git_folder = project.location / '.git'
    assert git_folder.exists()
