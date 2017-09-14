"""
Class representation of an application object, as read from a docker-stack file
"""
__author__ = 'tinglev@kth.se'

import re
import os
import json
import logging
import hashlib
import yaml
from everest_util.entities.service import Service
from everest_util.entities.cluster import Cluster
from everest_util.base_exception import EverestException
from everest_util.regex import Regex

class ApplicationException(EverestException):
    """
    Raised when an error occurs during application processing
    """
    pass

class ApplicationJsonEncoder(json.JSONEncoder):
    def default(self, o): # pylint: disable=E0202
        if hasattr(o, 'default'):
            return o.default()
        else:
            return json.JSONEncoder.default(self, o)

class Application(object):
    """
    The class
    """

    def __init__(self, registry, application_root_path):
        """
        Constructor

        Args:
            registry: dependency injected Registry class
            application_root_path: the root path directory of the calling application
        """
        self.registry = registry
        self._file_path = None
        self._application_name = None
        self._cluster = None
        self._yaml_content = None
        self._raw_file_content = None
        self._file_content_md5 = None
        self._services = []
        self.application_root_path = application_root_path
        self.log = logging.getLogger(__name__)

    def default(self):
        """
        JSONEncoder override

        Returns:
            json: a json representation of this class
        """
        return dict(application_name=self._application_name,
                    cluster=self._cluster,
                    service_file_md5=self._file_content_md5,
                    services=self._services)

    def init_from_service_file(self, service_file_path):
        """
        Initializes an instance of the class from a service file (docker-stack.yml)

        Args:
            service_file_path: the path to the file to initialize from

        Raises:
            ApplicationException: on error during initialization
        """
        try:
            self.log.debug('Initializing application from file "%s"', service_file_path)
            self._file_path = service_file_path
            self._parse_application_name()
            self._parse_file_contents()
            tmp_cluster = Cluster(self.application_root_path)
            self._cluster = tmp_cluster.init_from_service_file(service_file_path)
            self._init_services()
            self._calculate_md5()
            return self
        except Exception as error:
            raise ApplicationException('Unhandled exception when initializing application',
                                       ex=error)

    def get_file_path(self):
        """
        Getter for the file path
        """
        return self._file_path

    def get_application_dir(self):
        """
        Getter for the application directory
        """
        return os.path.dirname(self._file_path)

    def get_cluster_name(self):
        """
        Getter for the name of the cluster
        """
        return self._cluster.get_name()

    def get_cluster_env(self):
        """
        Getter for the string representation of the cluster environment
        """
        return str(self._cluster.get_env())

    def get_name(self):
        """
        Getter for the name of the application
        """
        return self._application_name

    def get_cluster(self):
        """
        Getter for the Cluster class instance
        """
        return self._cluster

    def get_env(self):
        """
        Returns a bash compatible string of environment variables and their
        values for this applicatino (concatenates all service environments)
        """
        return ' '.join([str(service.get_env()) for service in self._services])

    def get_md5(self):
        """
        Getter for the md5 hash of the file contents
        """
        return self._file_content_md5

    def get_services(self):
        """
        Getter for the list of Service class instances
        """
        return self._services

    def __str__(self):
        """
        ToString override
        """
        return ('(application: "{}", cluster: "{}")'
                .format(self.get_name(), self.get_cluster().get_name()))

    def __eq__(self, application):
        """
        Equality operator override
        """
        return (self.cache_equals(application) and
                self.get_services() == application.get_services())

    def cache_equals(self, application):
        """
        Equality helper function for two applications

        Args:
            application: the application to compare equality with
        """
        return (self.get_name() == application.get_name() and
                self.get_cluster() == application.get_cluster())

    def _calculate_md5(self):
        """
        Calculates an md5 hash of the file contents associated with this application
        """
        self._file_content_md5 = hashlib.md5(self._raw_file_content).hexdigest()

    def _parse_file_contents(self):
        """
        Parses the contents of the associated service file (docker-stack.yml) as
        yaml data and saves it to a member variable

        Raises:
            ApplicationException: on unable to read service file or when unable to
                                  parse contents as yaml
        """
        try:
            with open(self._file_path, 'r') as stream:
                self._raw_file_content = stream.read()
                stream.seek(0)
                self._yaml_content = yaml.load(stream)
        except IOError as err:
            raise ApplicationException('Unable to load file "{}"'.format(self._file_path,), err)
        except yaml.YAMLError as err:
            raise ApplicationException('Unable to parse yaml in file "{}"'
                                       .format(self._file_path,), err)

    def _parse_application_name(self):
        """
        Parses the application name from the service file path

        Returns:
            Nothing (sets member variable)

        Raises:
            ApplicationException: if unable to parse application name
        """
        match = re.search(Regex.get_registry_app_and_cluster(), self._file_path)
        if match:
            self._application_name = match.group(1)
            return
        raise ApplicationException('Could not get appplication name from service file path "{}"'
                                   .format(self._file_path))

    def _get_stack_services(self):
        """
        Creates an array of tuples on the format [(service name), (service data), ..] for
        each service in the yaml contents parsed

        Returns:
            an array of tuples: each service and its data
        """
        return [(name, service_struct)
                for (name, service_struct)
                in self._yaml_content['services'].iteritems()]

    def _init_services(self):
        """
        Initializes all services in the yaml contents parsed

        Returns:
            Nothing (adds services to the _services member variable)
        """
        services = self._get_stack_services()
        self.log.debug('Application has %i services', len(services))
        for name, service_struct in services:
            self._services.append(Service(self.registry)
                                  .init_from_stack_service(name, service_struct))
