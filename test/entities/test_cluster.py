__author__ = 'tinglev@kth.se'

import unittest
import json
import os
import StringIO
from mock import patch
from everest_util.paths import Paths
from everest_util.entities.cluster import Cluster, ClusterException
from everest_util.entities.application import ApplicationJsonEncoder
import root_path

class ClusterTests(unittest.TestCase):

    def test_equal(self):
        c1 = Cluster(root_path.get_root_path())
        c1._name = 'stage'
        c2 = Cluster(root_path.get_root_path())
        c2._name = 'stage'
        self.assertEqual(c1, c2)
        c2._name = 'active'
        self.assertNotEqual(c1, c2)

    def test_to_json(self):
        cluster = Cluster(root_path.get_root_path())
        cluster._name = 'stage'
        cluster._env_list.add_env('ENV_KEY1', 'ENV_VALUE1')
        cluster._env_list.add_env('ENV_KEY2', '"ENV AS STRING"')
        expected = {'cluster_name': 'stage',
                    'environment': [{'key': 'ENV_KEY1', 'value': 'ENV_VALUE1'},
                                    {'key': 'ENV_KEY2', 'value': '"ENV AS STRING"'}]}
        self.assertEqual(json.loads(ApplicationJsonEncoder().encode(cluster)), expected)

    def test_set_cluster_name(self):
        service_file_path = ('{}/cellus-registry/deploy/kth-azure-app/stage/docker-stack.yml'
                             .format(root_path.get_root_path()))
        cluster = Cluster(root_path.get_root_path())
        cluster._file_path = service_file_path
        cluster._set_cluster_name()
        self.assertEqual(cluster._name, 'stage')
        cluster._file_path = '/nope/'
        self.assertRaises(ClusterException, cluster._set_cluster_name)

    @patch.object(Paths, 'get_registry_deploy_path')
    def test_set_env_file_path(self, mock_deploy_path):
        path = os.path.dirname(os.path.realpath(__file__))
        mock_deploy_path.return_value = path
        cluster = Cluster(root_path.get_root_path())
        cluster._name = 'test'
        cluster._set_env_file_path()
        self.assertEqual(cluster._env_file_path, '{}/test-environment.env'.format(path))
        mock_deploy_path.return_value = 'no/nope'
        self.assertRaises(ClusterException, cluster._set_env_file_path)

    def test_matched_env_lines(self):
        cluster = Cluster(root_path.get_root_path())
        string_handle = StringIO.StringIO()
        string_handle.write('ENV_1=VALUE_1\n')
        string_handle.write('ENV_2=VALUE_2\n')
        string_handle.write('SERVICE_EXTENSIONS_FILE=../../development-service-extensions.yml\n')
        string_handle.write('#SHOULD_NOT_WORK=123\n')
        string_handle.write('[this shouldn\'t work either]')
        string_handle.seek(0)
        self.assertEqual(cluster._matched_env_lines(string_handle),
                         [('ENV_1', 'VALUE_1'),
                          ('ENV_2', 'VALUE_2'),
                          ('SERVICE_EXTENSIONS_FILE', '../../development-service-extensions.yml')])

    def test_raise_on_bad_cluster(self):
        cluster = Cluster(root_path.get_root_path())
        os.environ['USE_CLUSTERS'] = 'development'
        cluster._name = 'development'
        try:
            cluster._raise_on_bad_cluster()
        except:
            self.assertTrue(False)
        cluster._name = 'test'
        self.assertRaises(ClusterException, cluster._raise_on_bad_cluster)
