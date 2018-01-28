
import os

import py
from cookiecutter.main import cookiecutter


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

        result = cookiecutter(
            template=self.path,
            output_dir=output_dir,
            extra_context=self.variables,
            no_input=True,
            overwrite_if_exists=True,
        )

        return result
