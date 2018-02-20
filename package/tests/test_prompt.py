
import pytest
import py

from masonry.objects.cli import CLI


@pytest.fixture
def project_templates_path():
    return (
        py.path.local(__file__)
        .dirpath()
        .join('example_templates/simple_project')
    )


@pytest.fixture
def config(tmpdir, project_templates_path):

    config = {
        "application_data": tmpdir.join('application_data').strpath,
        "known_projects": {
            "simple_project": project_templates_path,
            "data_science": "another/path/here"
        },
    }
    return config


@pytest.fixture(autouse=True)
def no_prompts(monkeypatch):

    import inquirer

    def mock_inquirer_prompt(questions):
        answers = {q.name: q.default for q in questions}
        return answers

    # Mock the interactive input and use cookiecutter defaults instead
    monkeypatch.setattr(inquirer, 'prompt', mock_inquirer_prompt)


def test_cli_init_prompt(project_templates_path, config, tmpdir):

    # Given just the init command
    argument_string = f"init -o {tmpdir.strpath}"
    app = CLI(argument_string, config=config)
    args = app._validate_args()

    project_name = app._prompt_init_project(default="simple_project")

    assert project_name == 'simple_project'
