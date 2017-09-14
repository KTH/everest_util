"""
Representation of an image in a docker-stack file
"""
__author__ = 'tinglev@kth.se'

import json

class Image(object):
    """
    Image class
    """

    def __init__(self):
        """
        Constructor
        """
        self._name = None
        self._registry = None
        self._static_version = None
        self._semver_version = None
        self._is_semver = False
        self._version_env_key = None

    def default(self):
        """
        JSONEncoder override

        Returns:
            json: a json representation of this class
        """
        return dict(image_name=self._name,
                    static_version=self._static_version,
                    semver_version=self._semver_version)

    def __eq__(self, image):
        """
        Equality operator override
        """
        return (self.get_name() == image.get_name() and
                self.get_static_version() == image.get_static_version() and
                self.get_semver_version() == image.get_semver_version())

    def set_registry(self, registry):
        """
        Setter for the registry attribute
        """
        self._registry = registry

    def get_registry(self):
        """
        Getter for the registry attribute
        """
        return self._registry

    def set_name(self, name):
        """
        Setter for the name attribute
        """
        self._name = name

    def get_name(self):
        """
        Getter for the name attribute
        """
        return self._name

    def set_static_version(self, version):
        """
        Setter for the static version attribute
        """
        self._static_version = version

    def get_static_version(self):
        """
        Getter for the static version attribute
        """
        return self._static_version

    def set_semver_version(self, version):
        """
        Setter for the semver version attribute
        """
        self._semver_version = version

    def get_semver_version(self):
        """
        Getter for the semver version attribute
        """
        return self._semver_version

    def set_is_semver(self, value):
        """
        Setter for the is semver flag
        """
        self._is_semver = value

    def get_is_semver(self):
        """
        Getter for the is semver flag
        """
        return self._is_semver

    def set_version_env_key(self, env_key):
        """
        Setter for the version env key attribute
        """
        self._version_env_key = env_key

    def get_version_env_key(self):
        """
        Getter for the version env key attribute
        """
        return self._version_env_key
