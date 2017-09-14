"""
Class representation of a cluster object
"""
__author__ = 'tinglev@kth.se'

import re
import os
import logging
import json
from everest_util.paths import Paths
from everest_util.entities.environment_list import EnvironmentList
from everest_util.regex import Regex
from everest_util.base_exception import BaseException

class ClusterException(BaseException):
    """
    Exception raised when errors occur during cluster processing
    """
    pass

class Cluster(json.JSONEncoder):
    """
    The class
    """

    USE_CLUSTERS_ENV_VAR = 'USE_CLUSTERS'

    def __init__(self, project_root_path):
        """
        Constructor

        Args:
            use_clusters_env_var: the name of the environment variable which contains a colon
                                  separated list of clusters to use
        """
        self._name = None
        self._file_path = None
        self._env_file_path = None
        self._env_list = EnvironmentList()
        self.log = logging.getLogger(__name__)
        self.project_root_path = project_root_path
        super(Cluster, json.JSONEncoder).__init__(self)

    def init_from_service_file(self, service_file_path):
        """
        Initializes this cluster from a given service file (docker-stack.yml)

        Args:
            service_file_path: the path to the docker-stack file
        """
        self.log.debug('Initializing cluster from file "%s"', service_file_path)
        self._file_path = service_file_path
        self._set_cluster_name()
        self._raise_on_bad_cluster()
        self._set_env_file_path()
        self._read_environment_from_file()
        return self

    def default(self, o): # pylint: disable=E0202
        """
        JSONEncoder override

        Returns:
            json: a json representation of this class
        """
        return dict(cluster_name=self._name, environment=self._env_list)

    def get_name(self):
        """
        Getter for the name attribute

        Returns:
            string: the name of the cluster
        """
        return self._name

    def get_env(self):
        """
        Getter for the environment list attribute

        Returns:
            EnvironmentList: a list of environment variables for this cluster
        """
        return self._env_list

    def get_use_clusters_env_var(self):
        """
        Getter for the use cluster environment variable name attribute

        Returns:
            string: the name of the environment variable for used clusters
        """
        return Cluster.USE_CLUSTERS_ENV_VAR

    def __eq__(self, cluster):
        """
        Equality operator override
        """
        return self.get_name() == cluster.get_name()

    def _use_cluster(self):
        """
        Determines wether or not this cluster should be used for deployments,
        as set by the USE_CLUSTERS_ENV_VAR environment variable

        Returns:
            boolean: true if this cluster should be used for deployments, else false
        """
        use_clusters = os.environ.get(self.get_use_clusters_env_var())
        if not use_clusters:
            return True
        if self.get_name() in use_clusters.split(','):
            return True
        return False

    def _raise_on_bad_cluster(self):
        """
        Raises a cluster exception if this cluster should not be used for deployments

        Raises:
            ClusterException: if this cluster is missing from the USE_CLUSTERS_ENV_VAR
                              environment variable
        """
        if not self._use_cluster():
            raise ClusterException('Cluster is not listed in environment variable "{}". '
                                   'The value of the env var is "{}"'
                                   .format(self.get_use_clusters_env_var(),
                                           os.environ.get(self.get_use_clusters_env_var())))

    def _set_cluster_name(self):
        """
        Parses the cluster name from the docker-stack file path

        Returns:
            Nothing (sets member variable)

        Raises:
            ClusterException: if the cluster name was unable to be parsed
                              from the file path
        """
        match = re.search(Regex.get_cellus_registry_cluster(), self._file_path)
        if match:
            self._name = match.group(1)
            return
        raise ClusterException('Could not get cluster name from service file path "{}"'
                               .format(self._file_path))

    def _get_env_file_name(self):
        """
        Gets the environment file name for this cluster

        Returns:
            string: the name of the cluster environment file
        """
        return '{}-environment.env'.format(self._name)

    def _set_env_file_path(self):
        """
        Calculates the complete file path for this clusters environment file

        Returns:
            Nothing (sets member variable)

        Raises:
            ClusterException: When the calculated environment file does not exist
        """
        env_file_path = '{}/{}'.format(Paths.get_registry_deploy_path(self.project_root_path),
                                       self._get_env_file_name())
        if os.path.isfile(env_file_path):
            self._env_file_path = env_file_path
            return
        raise ClusterException('Cluster env file "{}" does not exist'.format(env_file_path))

    def _read_environment_from_file(self):
        """
        Reads this clusters environment file to a EnvironmentList class instance

        Raises:
            ClusterException: on error while reading the environment file
        """
        self.log.debug('Reading cluster environment from: "%s"', self._env_file_path)
        try:
            with open(self._env_file_path, 'r') as env_file:
                envs = self._matched_env_lines(env_file)
            for env in envs:
                self._env_list.add_env(env[0], env[1])
            self.log.debug('Found %i valid environment variables for cluster', len(self._env_list))
        except IOError as io_err:
            raise ClusterException('Error while reading cluster environment file "{}"'
                                   .format(self._env_file_path), io_err)

    def _matched_env_lines(self, file_handle):
        """
        Reads a file handle and returns an array of tuples with all valid environment variables
        found in the file

        Args:
            file_handle: the file handle to the file to be read

        Returns:
            array of tuples: an array of tuples with the format [(env_key, env_val),..]
        """
        env_regex = Regex.get_label_and_env_regex()
        return [(line.split('=')[0], line.split('=')[1].rstrip('\n'))
                for line in file_handle.readlines()
                if re.match(env_regex, line)]
