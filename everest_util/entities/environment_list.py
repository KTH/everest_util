"""
Class representation of a list of environment variables
"""
__author__ = 'tinglev@kth.se'

class EnvironmentList(object):
    """
    The class
    """

    def __init__(self):
        """
        Constructor
        """
        self._env_list = []

    def to_json(self):
        """
        Returns a JSON representation of the environment variable list
        Returns:
            json array: an array containing environment variables on the format KEY=VALUE
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
