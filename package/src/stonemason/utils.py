

import os 
from pathlib import Path

import json


def postfix(original_file, new_file):
    """ Add the content of new_content to the end of original_file and remove new_content """

    with open(original_file, 'a') as fout:
        with open(new_file) as fin:
            fout.write(fin.read())
    os.remove(fin.name)


def prefix(original_file, new_file):
    """ Add the content of new_content to the end of original_file and remove new_content """

    with open(new_file, 'a') as fout:
        with open(original_file) as fin:
            fout.write(fin.read())
    os.remove(fin.name)
    os.rename(fout.name, fin.name)


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
