"""
Path helpers
"""

__author__ = 'tinglev@kth.se'

import os

class Paths(object):
    """
    Static object for all library methods
    """

    @staticmethod
    def get_file_directory(file_path):
        """
        Get the directory of a given file. Should be
        called with __file__ as the only argument.
        Args:
            file_path: __file__
        Returns:
            string: the name of the directory containing the file
        Raises:
            OSError: on path or file error
        """
        return os.path.dirname(os.path.abspath(file_path))
