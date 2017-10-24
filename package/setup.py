#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'masonry'
DESCRIPTION = 'A command line tool for composable project templating.'
URL = 'https://github.com/MrKriss/masonry'
EMAIL = 'chris.j.musselle@gmail.com'
AUTHOR = 'Chris Musselle'

REQUIRED = [
    'cookiecutter>=1.6',
    'docopt',
    'schema',
    'inquirer',
    'ruamel.yaml>=0.15',
    'gitpython',
    'clint',
    'py'
]

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in file!
with io.open(os.path.join(repo_root, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(repo_root, 'package', 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    # Metadata
    name=NAME,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    # Use version control to define version tag
    use_scm_version={"root": "..", "relative_to": __file__},
    # Package Locations
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    # Dependencies
    install_requires=REQUIRED,
    include_package_data=True,

    # Entry Point for the command line application
    entry_points={
        'console_scripts': ['mason=masonry.main:main']
    },
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
    ],
    # Command for setup.py publishing support.
    cmdclass={
        'upload': UploadCommand,
    },
)
