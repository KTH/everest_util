"""
Path helpers
"""

__author__ = 'tinglev@kth.se'

import os

class Paths(object):
    """
    Static object for all library methods
    """

    CELLUS_REGISTRY_DIR_NAME = 'cellus-registry'
    DEPLOY_SUB_DIR_NAME = 'deploy'

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
    
    @staticmethod
    def get_registry_dir_name():
        """
        Returns the name of the directory for cellus-registry

        Returns:
            string: the name of the directory for cellus-registry
        """
        return Paths.CELLUS_REGISTRY_DIR_NAME

    @staticmethod
    def get_deploy_dir_name():
        """
        Returns the name of the deployment directory withing cellus-registry

        Returns:
            string: the name of the deployment directory
        """
        return Paths.DEPLOY_SUB_DIR_NAME

    @staticmethod
    def get_registry_path(project_root_path):
        """
        Return the full, absolute path to the cellus-registry dir
        contained within the calling application

        Args:
            project_root_path: the root path of the calling application

        Returns:
            string: the absolut path to cellus-registry
        """
        return '{}/{}'.format(project_root_path,
                              Paths.get_registry_dir_name())

    @staticmethod
    def get_registry_deploy_path(project_root_path):
        """
        Return the full, absolut path to the deploy directory within
        the cellus-registry directory within the calling application

        Args:
            project_root_path: the root path of the calling application

        Returns:
            string: the path to the cellus-registry deploy directory
        """
        return '{}/{}'.format(Paths.get_registry_path(project_root_path),
                              Paths.get_deploy_dir_name())
