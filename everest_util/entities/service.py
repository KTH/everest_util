"""
Class representation of a service object
"""
__author__ = 'tinglev@kth.se'

import logging
import re
import json
from everest_util.entities.image import Image
from everest_util.entities.environment_list import EnvironmentList
from everest_util.entities.label_list import LabelList
from everest_util.regex import Regex
from everest_util.version import Version
from everest_util.base_exception import EverestException
from everest_util.json_encoder import ApplicationJsonEncoder

class ServiceException(EverestException):
    """
    Exception raised when there is an error during the processing of the service
    """
    pass

class Service(object):
    """
    The class representation of a service object
    """

    def __init__(self, registry):
        """
        Constructor
        Args:
            registry: dependecy injected Registry class to use
        """
        self._service_struct = None
        self._name = None
        self._image = Image()
        self._env_list = EnvironmentList()
        self._deploy_labels = LabelList()
        self._labels = LabelList()
        self.registry = registry
        self.log = logging.getLogger(__name__)

    def init_from_stack_service(self, name, service_struct):
        """
        Initializes an instance of the class given a name and the parsed contents
        of a docker-stack file

        Args:
            name: the name of the service
            service_struct: the parsed (as json) contents of a docker-stack file

        Raises:
            ServiceException: on failure during initialization
        """
        self.log.debug('Initializing service with name "%s"', name)
        self._service_struct = service_struct
        self._name = name
        self._parse_image_info()
        self._parse_semver_version()
        self._fetch_semver_version()
        self._parse_labels()
        self._parse_deploy_labels()
        self._create_environment_list()
        return self

    def get_env(self):
        """
        Getter for the environment list attribute

        Returns:
            EnvironmentList: the list of environment variables for this service
        """
        return self._env_list

    def get_name(self):
        """
        Getter for the name of this service

        Returns:
            string: the name
        """
        return self._name

    def get_image(self):
        """
        Getter for the image associated with this service

        Returns:
            Image: the image class
        """
        return self._image

    def get_resources(self):
        """
        Getter for the deploy resources of this service, according to the docker-stack file

        Returns:
            json: a json object
        """
        return self._service_struct['deploy']['resources']

    def get_restart_policy(self):
        """
        Getter for the restart policy of this service

        Returns:
            json: a json object
        """
        return self._service_struct['deploy']['restart_policy']

    def get_logging_policy(self):
        """
        Getter for the logging policy of this object

        Returns:
            json: a json object
        """
        return self._service_struct['logging']

    def __eq__(self, service):
        """
        Equality operator override
        """
        return (self.get_name() == service.get_name() and
                self.get_image() == service.get_image())

    def default(self):
        """
        JSONEncoder override

        Returns:
            json: a json representation of this class
        """
        return dict(service_name=self._name, environment=self._env_list,
                    labels=self._labels, deploy_labels=self._deploy_labels,
                    image=self._image)

    def deserialize(self, json_string):
        """
        Deserializes this object from a valid json string

        Args:
            json_string: a string containing valid json

        Returns:
            self: for chaining purposes
        """
        json_data = json.loads(json_string)
        self._name = json_data['service_name']
        image_string = json.dumps(json_data['image'], cls=ApplicationJsonEncoder)
        if json_data['environment']:
            env_string = json.dumps(json_data['environment'], cls=ApplicationJsonEncoder)
            self._env_list.deserialize(env_string)
        if json_data['labels']:
            label_string = json.dumps(json_data['labels'], cls=ApplicationJsonEncoder)
            self._labels.deserialize(label_string)
        if json_data['deploy_labels']:
            deploy_string = json.dumps(json_data['deploy_labels'], cls=ApplicationJsonEncoder)
            self._deploy_labels.deserialize(deploy_string)
        self._image.deserialize(image_string)
        return self

    def _create_environment_list(self):
        if self._image.get_is_semver():
            self._env_list.add_env(self._image.get_version_env_key(),
                                   self._image.get_semver_version())
        self._parse_environment()


    def _is_valid_label(self, label):
        return re.match(Regex.get_label_and_env_regex(), label)

    def _parse_deploy_labels(self):
        try:
            map(lambda (l, v): self._deploy_labels.add_label(l, v), [
                (label.split('=')[0], label.split('=')[1].strip('"'))
                for label in self._service_struct['deploy']['labels']
                if self._is_valid_label(label)
            ])
        except KeyError as key_err:
            self.log.debug('Service "%s" has no service deploy labels. '
                           'Key missing: %s', self.get_name(), key_err)
            raise ServiceException('Service "{}" has no service deploy labels. '
                                   'Key missing: "{}"'.format(self.get_name(), key_err)
                                   , ex=key_err)

    def _parse_labels(self):
        try:
            map(lambda (l, v): self._labels.add_label(l, v), [
                (label.split('=')[0], label.split('=')[1].strip('"'))
                for label in self._service_struct['labels']
                if self._is_valid_label(label)
            ])
        except KeyError as key_err:
            self.log.debug('Service "%s" has no service root labels. Key missing: %s',
                           self.get_name(), key_err)
            raise ServiceException('Service "{}" has no service root labels. Key missing: {}'
                                   .format(self.get_name(), key_err),
                                   ex=key_err)

    def _parse_environment(self):
        try:
            map(lambda (l, v): self._env_list.add_env(l, v), [
                (env.split('=')[0], env.split('=')[1])
                for env in self._service_struct['environment']
                if self._is_valid_label(env)
            ])
        except KeyError as key_err:
            self.log.debug('Service "%s" has no environment. Key missing: %s', self._name, key_err)
            raise ServiceException('Service "%s" has no environment. Key missing: %s',
                                   ex=key_err)

    def _fetch_semver_version(self):
        if self._image.get_is_semver():
            semver_version = self._get_env_value_from_struct(self._image.get_version_env_key())
            self.log.debug('Semver version before lookup is "%s"', semver_version)
            registry_tags = self.registry.get_image_tags(self._image.get_name())
            self.log.debug('Got tags from registry: "%s"', registry_tags)
            valid_versions = Version.get_sorted_valid_versions(registry_tags)
            self.log.debug('After sort and validation: "%s"', valid_versions)
            final_semver_version = Version.get_best_semver_match(valid_versions, semver_version)
            self.log.debug('Setting semver version to "%s"', final_semver_version)
            self._image.set_semver_version(final_semver_version)

    def _get_env_value_from_struct(self, env_key):
        try:
            return self._service_struct['environment'][env_key]
        except KeyError as key_err:
            self.log.debug('Could not fetch environment key "%s" for service "%s"'
                           , env_key, self._name)
            raise ServiceException('Could not fetch environment key "{}" for service "{}"'
                                   .format(env_key, self._name), ex=key_err)

    def _parse_semver_version(self):
        match = re.match(Regex.get_env_var_dereference_regex(),
                         self._image.get_static_version())
        if match:
            self.log.debug('Service has semver version "%s" with env key "%s"',
                           self._image.get_static_version(), match.group(1))
            self._image.set_is_semver(True)
            self._image.set_version_env_key(match.group(1))
            return
        self.log.debug('Service has static image version "%s"',
                       self._image.get_static_version())

    def _parse_image_info(self):
        try:
            image = self._service_struct['image']
            self._parse_image_registry(image)
            self._parse_image_name(image)
            self._parse_image_version(image)
        except KeyError as key_err:
            self.log.debug('Missing image section for service "%s"',
                           self._name)
            raise ServiceException('Missing image section for service "{}"'
                                   .format(self._name), key_err)

    def _parse_image_registry(self, image):
        match = re.match(Regex.get_image_and_registry_regex(), image)
        if match:
            self._image.set_registry(match.group(1))
            return
        self._image.set_registry(None)
        self.log.debug('Image is external (contains no registry)')

    def _parse_image_name(self, image):
        match = re.match(Regex.get_image_parts_regex(), image)
        if match:
            self._image.set_name(match.group(2))
            return
        self.log.debug('Could not parse image name from image section: "%s"',
                       image)
        raise ServiceException('Could not parse image name from image section: "{}"'
                               .format(image))

    def _parse_image_version(self, image):
        match = re.match(Regex.get_image_parts_regex(), image)
        if match:
            self._image.set_static_version(match.group(3))
            return
        self.log.debug('Could not parse image name from image section: "%s"',
                       image)
        raise ServiceException('Could not parse image version from image section: "{}"'
                               .format(image))
