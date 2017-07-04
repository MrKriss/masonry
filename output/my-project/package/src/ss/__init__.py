
from pkg_resources import get_distribution, DistributionNotFound
import pathlib

# Code to lookup version number as obtained from setuptools_scm
# https://pypi.python.org/pypi/setuptools_scm
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = None

# Store location of where the package is installed
PKG_DIR = pathlib.Path(__file__).parent