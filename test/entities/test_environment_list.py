__author__ = 'tinglev@kth.se'

import unittest
import json
from mock import patch
from everest_util.entities.environment_list import EnvironmentList
from everest_util.json_encoder import ApplicationJsonEncoder

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
        env_list1 = EnvironmentList()
        env_list1.add_env('ENV_KEY', 'ENV_VALUE')
        env_list1.add_env('ENV_KEY', '"ENV WITH SPACE"')
        env_list2 = EnvironmentList().deserialize(json.dumps(env_list1, cls=ApplicationJsonEncoder))
        self.assertEqual(env_list1, env_list2)