
# Std libs
import os
import sys

# Data Analysis
import pandas as pd
import numpy as np

# Use python-dotenv to manage environment variables
from dotenv import load_dotenv, find_dotenv

from dotenv import load_dotenv, find_dotenv

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables
load_dotenv(dotenv_path)

database_url = os.environ.get("DATABASE_URL")
other_variable = os.environ.get("OTHER_VARIABLE")
