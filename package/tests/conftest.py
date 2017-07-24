

import pytest
from pathlib import Path
import json


TEST_DIR = Path(__file__).parent


@pytest.fixture(autouse=True)
def no_prompts(monkeypatch):

    import inquirer

    def mock_inquirer_prompt(questions):
        answers = {q.name: q.default for q in questions}
        return answers

    # Mock the interactive input and use cookiecutter defaults instead
    monkeypatch.setattr(inquirer, 'prompt', mock_inquirer_prompt)