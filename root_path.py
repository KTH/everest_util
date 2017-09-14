"""
Module used to allow access to projet root path
"""
__author__ = 'tinglev@kth.se'

import os

def get_root_path():
    """
    Gets this files directory, which is the root directory of
    the entire project

    Returns:
        string: path to the root directory of everest_util
    """
    return os.path.dirname(os.path.realpath(__file__))
