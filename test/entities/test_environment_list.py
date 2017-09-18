__author__ = 'tinglev@kth.se'

import unittest
import json
from mock import patch
from everest_util.entities.environment_list import EnvironmentList
from everest_util.entities.application import ApplicationJsonEncoder

class EnvironmentListTests(unittest.TestCase):

    def test_add_env(self):
        env_list = EnvironmentList()
        self.assertEqual(env_list._env_list, [])
        env_list.add_env('ENV_KEY', 'ENV_VALUE')
        self.assertEqual(env_list._env_list, [{'key':'ENV_KEY','value':'ENV_VALUE'}])
        env_list.add_env('ENV_KEY', '"ENV WITH SPACE"')
        self.assertEqual(env_list._env_list, [{'key':'ENV_KEY', 'value':'ENV_VALUE'},
                                              {'key':'ENV_KEY', 'value':'"ENV WITH SPACE"'}])

    def test_to_string(self):
        env_list = EnvironmentList()
        env_list.add_env('ENV_KEY', 'ENV_VALUE')
        self.assertEqual(str(env_list), 'ENV_KEY=ENV_VALUE')
        env_list.add_env('ENV_KEY', '"ENV WITH SPACE"')
        self.assertEqual(str(env_list), 'ENV_KEY=ENV_VALUE ENV_KEY="ENV WITH SPACE"')

    def test_to_json(self):
        env_list = EnvironmentList()
        env_list.add_env('ENV_KEY', 'ENV_VALUE')
        self.assertEqual(env_list.default(), [{'key': 'ENV_KEY', 'value': 'ENV_VALUE'}])
        env_list.add_env('ENV_KEY', '"ENV WITH SPACE"')
        self.assertEqual(json.loads(json.dumps(env_list, cls=ApplicationJsonEncoder)),
                         [{'key': 'ENV_KEY', 'value': 'ENV_VALUE'},
                          {'key': 'ENV_KEY', 'value': '"ENV WITH SPACE"'}])

    def test_deserialize(self):
        env_list = EnvironmentList()
        json_string = '[{"key":"key1", "value":"value1"},{"key":"key2", "value":"value2"}]'
        env_list.deserialize(json_string)
        self.assertEqual(env_list._env_list[0]['key'], 'key1')
        self.assertEqual(len(env_list), 2)
