
import json
import logging
import os
import shlex
import subprocess
from itertools import dropwhile
from pathlib import Path

from clint.textui import colored, indent, puts


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

    json.dump(obj, template_metadata_path.open('w'), indent=4)


def rindex(lst, item):
    """Return the index position of the last item in a list."""
    def index_ne(x):
        return lst[x] != item
    try:
        return next(dropwhile(index_ne, reversed(range(len(lst)))))
    except StopIteration:
        raise ValueError("rindex(lst, item): item not in list")


def setup_logger(name=__name__, logfile=None, level=logging.DEBUG):
    """
    A utility function that you can call to easily set up logging to the
    console and optionally to a file. No hassles.
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(level)

    # Remove old handlers to allow updating settings
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    # create console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)  # propagate all messages

    # add the formatter to the handler
    formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s')
    stream_handler.setFormatter(formatter)

    # setup logger and add the handlers
    logger.addHandler(stream_handler)

    if logfile:
        filehandler = logging.FileHandler(logfile)
        filehandler.setLevel(logging.NOTSET)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)

    logger.debug("logger set up. level=%d", level)
    return logger


def run_and_capture(command, give_feedback=True):

    p = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if p.returncode != 0 and give_feedback:
        puts(colored.red('Error in executing "%s"' % command))
        puts(colored.red(p.stderr.decode().strip()))
    elif p.returncode == 0 and give_feedback:
        puts(colored.green('Executed "%s"' % command))

    return p
