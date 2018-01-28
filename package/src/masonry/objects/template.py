from cookiecutter.config import get_user_config
from cookiecutter.generate import generate_context, generate_files
from cookiecutter.exceptions import InvalidModeException
from cookiecutter.prompt import prompt_for_config
from cookiecutter.replay import dump, load
from cookiecutter.repository import determine_repo_dir

import os


class Template:

    """ Responsible for storing cookicutter template information and triggering rendering of the template """

    def __init__(self, path, variables):
        self.path = path
        self.variables = variables

    def render(self, output_dir):
        """ Run Cookiecutter just as if using it from the command line. """

        from cookiecutter.main import cookiecutter

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
            template=self.path.strpath,
            output_dir=output_dir,
            extra_context=self.variables,
            no_input=True,
            overwrite_if_exists=True,
        )

        return result


# class CookiecutterRenderer():

#     """ Defines the specific way the template is rendered """

#     def __init__(self, *parameter_list):
#         pass

#     def render(template_path, variables):

#         from cookiecutter.main import cookiecutter

#         result = cookiecutter(
#             template=template_path,
#             no_input=True,
#             extra_context=variables
#         )
#         return result

#     def render(
#             template, checkout=None, no_input=False, extra_context=None,
#             replay=False, overwrite_if_exists=False, output_dir='.',
#             config_file=None, default_config=False, password=None):
#         """ Render cookiecutter template and return path and rendered context

#         The API equivalent to using Cookiecutter at the command line.

#         :param template: A directory containing a project template directory,
#             or a URL to a git repository.
#         :param checkout: The branch, tag or commit ID to checkout after clone.
#         :param no_input: Prompt the user at command line for manual configuration?
#         :param extra_context: A dictionary of context that overrides default
#             and user configuration.
#         :param: overwrite_if_exists: Overwrite the contents of output directory
#             if it exists
#         :param output_dir: Where to output the generated project dir into.
#         :param config_file: User configuration file path.
#         :param default_config: Use default values rather than a config file.
#         """
#         if replay and ((no_input is not False) or (extra_context is not None)):
#             err_msg = (
#                 "You can not use both replay and no_input or extra_context "
#                 "at the same time."
#             )
#             raise InvalidModeException(err_msg)

#         config_dict = get_user_config(
#             config_file=config_file,
#             default_config=default_config,
#         )

#         repo_dir, cleanup = determine_repo_dir(
#             template=template,
#             abbreviations=config_dict['abbreviations'],
#             clone_to_dir=config_dict['cookiecutters_dir'],
#             checkout=checkout,
#             no_input=no_input,
#             password=password
#         )

#         template_name = os.path.basename(os.path.abspath(repo_dir))

#         if replay:
#             context = load(config_dict['replay_dir'], template_name)
#         else:
#             context_file = os.path.join(repo_dir, 'cookiecutter.json')
#             logger.debug('context_file is {}'.format(context_file))

#             context = generate_context(
#                 context_file=context_file,
#                 default_context=config_dict['default_context'],
#                 extra_context=extra_context,
#             )

#             # Add any previously rendered context variables in past templates
#             for k, v in extra_context.items():
#                 if k not in context['cookiecutter']:
#                     context['cookiecutter'][k] = v

#             # prompt the user to manually configure at the command line.
#             # except when 'no-input' flag is set
#             context['cookiecutter'] = prompt_for_config(context, no_input)

#             # include template dir or url in the context dict
#             context['cookiecutter']['_template'] = template

#             dump(config_dict['replay_dir'], template_name, context)

#         # Create project from local context and project template.
#         result = generate_files(
#             repo_dir=repo_dir,
#             context=context,
#             overwrite_if_exists=overwrite_if_exists,
#             output_dir=output_dir
#         )

#         return result, context['cookiecutter']
