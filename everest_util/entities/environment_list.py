"""
Class representation of a list of environment variables
"""
__author__ = 'tinglev@kth.se'

import json

class EnvironmentList(json.JSONEncoder):
    """
    The class
    """

    def __init__(self):
        """
        Constructor
        """
        self._env_list = []
        super(EnvironmentList, json.JSONEncoder).__init__(self)

    def default(self, o): # pylint: disable=E0202
        """
        JSONEncoder override

        Returns:
            json: a json representation of this class
        """
        return self._env_list

    def add_env(self, key, value):
        """
        Add an environment variable to the list

        Args:
            key: the key
            value: the value
        """
        self._env_list.append({'key':key, 'value':value})

    def __str__(self):
        """
        ToString operator override. Will print on the format "KEY1=VALUE1 KEY2=VALUE2 ..."
        """
        return ' '.join(['{}={}'.format(e['key'], e['value']) for e in self._env_list])

    def __len__(self):
        """
        Len operator override
        """
        return len(self._env_list)
