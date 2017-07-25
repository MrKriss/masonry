
import os 
from pathlib import Path

import json


def load_application_data(location=None):
    """Return the stored application data on where templates live"""

    if not location:
        location = os.getenv("HOME")

    app_data_dir = Path(os.path.join(location, ".stonemason"))

    template_metadata_path = app_data_dir / "templates.json"

    if template_metadata_path.exists():
        obj = json.loads(template_metadata_path.read_text())
    else:
        obj = {}

    return obj


def save_application_data(obj, location=None):
    """Save application data on where templates live"""

    if not location:
        location = os.getenv("HOME")

    app_data_dir = Path(os.path.join(location, ".stonemason"))
    app_data_dir.mkdir(exist_ok=True)

    template_metadata_path = app_data_dir / "templates.json"

    json.dump(obj, template_metadata_path.open('w'))
