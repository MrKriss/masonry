
import pytest
from masonry.template import Template
from pathlib import Path
import py.path


@pytest.fixture
def project_templates_path():
    return (
        py.path.local(__file__)
        .dirpath()
        .join('example_templates/simple_project')
    )


def test_can_create_template_and_render(project_templates_path, tmpdir):

    template_path = project_templates_path.join('first_layer')
    variables = {
        "project_name": "new-project",
        "file1_text": "Hello World!"
    }

    template = Template(template_path, variables)
    template.render(output_dir=tmpdir.strpath)

    project_path = tmpdir.join(variables['project_name'])
    created_file = project_path.join('file_from_layer_1.txt')

    assert project_path.check(dir=True)
    assert created_file.check(file=True)
    content = created_file.read_text('utf8')
    assert variables['file1_text'] in content
