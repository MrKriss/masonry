#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Im a doc sting!!!
"""

import sys
import os

from fileinput import FileInput

# Here are some data science libraries
import pandas as pd
import numpy as np

MY_CONSTANT = 12124


def my_new_first_function(arg1, arg2):
    """This is my doc string of things"""
    ans = arg1 * arg2
    return ans


# This function is important
def function1(arg1, arg2):
    """This is my doc string of things"""
    ans = arg1 + arg2
    return ans


def function2(arg1, arg2):
    """This is my doc string of things"""
    ans = f'  {arg1} + {arg2}  '
    return ans


def function3(arg1, arg2):
    """This is my doc string of things

    Here is an
    extended decription.
    """
    ans = arg1 + arg2
    return ans


if __name__ == '__main__':
    print(function1(5, 6))

    print(function2(5, 6))
