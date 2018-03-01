
import os

from pathlib import Path

import py
from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import FailedHookException, UndefinedVariableInTemplate

import shutil


class Template:

    """ Responsible for storing cookicutter template information and triggering rendering of the template """

    def __init__(self, path, variables):
        self.path = str(path)
        self.variables = variables

    def render(self, output_dir):
        """ Run Cookiecutter just as if using it from the command line. 

        Parameters
        ----------
        output_dir: str
            Where to output the generated project dir into.
        """

        # template:
        #     A directory containing a project template directory, or a URL to a git repository.
        # checkout:
        #     The branch, tag or commit ID to checkout after clone.
        # no_input:
        #     Prompt the user at command line for manual configuration?
        # extra_context:
        #    A dictionary of context that overrides default and user configuration.
        # overwrite_if_exists:
        #    Overwrite the contents of output directory if it exists
        # output_dir:
        #     Where to output the generated project dir into.
        # config_file:
        #     User configuration file path.
        # default_config:
        #     Use default values rather than a config file.
        # password:
        #     The password to use when extracting the repository.

        # Make Backup
        archive_file = os.path.join(output_dir, 'archive')
        archive_path = shutil.make_archive(
            base_name=archive_file,
            format='tar',
            root_dir=output_dir,
            base_dir='.'
        )

        result = None

        try:
            result = cookiecutter(
                template=self.path,
                output_dir=output_dir,
                extra_context=self.variables,
                no_input=True,
                overwrite_if_exists=True,
            )
        except (FailedHookException, UndefinedVariableInTemplate) as e:
            # Rollback to archived content
            print("An error occured during templating, Rolling back to last stable state.")
            clear_content(output_dir)
            shutil.unpack_archive(archive_path, output_dir)
            raise e
        finally:
            # Remove Backup
            os.remove(archive_path)

        return result


def clear_content(dir_path):
    """Remove all the content form a directory, leaving the archive backup file."""

    for dirpath, subdirs, filenames in os.walk(dir_path, topdown=False):

        for file in filenames:
            file_path = Path(dirpath) / file
            if file_path.name != 'archive.tar':
                file_path.unlink()

        for subdir in subdirs:
            subdir_path = Path(dirpath) / subdir
            subdir_path.rmdir()
