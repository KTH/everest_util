__author__ = 'tinglev@kth.se'

import os
import json
import unittest
from mock import patch
from everest_util.entities.application import Application, ApplicationJsonEncoder, ApplicationException
from everest_util.systems.registry import Registry
import test.entities.test_data as test_data
import root_path

class ApplicationTests(unittest.TestCase):

    def test_parse_application_name(self):
        app = Application(Registry('', '', ''), root_path.get_root_path())
        app._file_path = '/root/cellus/cellus-registry/deploy/kth-azure-app/stage/docker-stack.yml'
        app._parse_application_name()
        self.assertEqual(app.get_name(), 'kth-azure-app')
        app._file_path = 'deploy/kth-azure-app/stage/docker-stack.yml'
        self.assertRaises(ApplicationException, app._parse_application_name)

    def test_parse_file_contents(self):
        app = Application(Registry('', '', ''), root_path.get_root_path())
        app._file_path = '{}/docker-stack.yml'.format(os.path.dirname(os.path.realpath(__file__)))
        app._parse_file_contents()
        self.assertIsNotNone(app._yaml_content)
        self.assertIsNotNone(app._raw_file_content)
        self.assertTrue(len(app._yaml_content['services']), 2)
        app._file_path = 'blabla'
        self.assertRaises(ApplicationException, app._parse_file_contents)

    def test_get_stack_services(self):
        app = Application(Registry('', '', ''), root_path.get_root_path())
        app._file_path = ('{}/docker-stack.yml'.format(os.path.dirname(os.path.realpath(__file__))))
        app._parse_file_contents()
        result = app._get_stack_services()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], 'web')
        self.assertIsNotNone(result[0][1]['deploy'])

    def test_calculate_md5(self):
        app = Application(Registry('', '', ''), root_path.get_root_path())
        app._file_path = ('{}/docker-stack.yml'.format(os.path.dirname(os.path.realpath(__file__))))
        app._parse_file_contents()
        app._calculate_md5()
        self.assertEqual(app.get_md5(), '536b9794c3b718b3b280dfdb3497a540')

    def test_cache_equals(self):
        app1 = test_data.get_test_application()
        app2 = test_data.get_test_application()
        self.assertTrue(app1.cache_equals(app2))
        app2._application_name = 'nonono'
        self.assertFalse(app1.cache_equals(app2))
        app2 = test_data.get_test_application()
        app2._cluster._name = 'new_cluster'
        self.assertFalse(app1.cache_equals(app2))

    def test_equals(self):
        app1 = test_data.get_test_application()
        app2 = test_data.get_test_application()
        self.assertEqual(app1, app2)
        app1._services[1].get_image().set_static_version('5.4.3')
        self.assertNotEqual(app1, app2)
        app1 = test_data.get_test_application()
        app1._application_name = 'no'
        self.assertNotEqual(app1, app2)
        app1 = test_data.get_test_application()
        app1._services[0]._name = 'no_name'
        self.assertNotEqual(app1, app2)
        app1 = test_data.get_test_application()
        app1._services[0].get_image().set_semver_version('3.9.4')
        self.assertNotEqual(app1, app2)

    def test_to_json(self):
        app = test_data.get_test_application()
        app_as_json = json.loads(ApplicationJsonEncoder().encode(app))
        self.assertEqual(app_as_json['application_name'], 'kth-azure-app')
        self.assertEqual(app_as_json['cluster']['cluster_name'], 'stage')
        self.assertEqual(len(app_as_json['services']), 2)
        self.assertEqual(app_as_json['services'][0]['labels'][0]['label'], 'se.kth.label.bool')
        self.assertEqual(app_as_json['services'][0]['image']['image_name'], 'kth-azure-app')
        self.assertEqual(app_as_json['services'][0]['environment'][0]['key'], 'ENV_KEY1')

    def test_to_string(self):
        app = test_data.get_test_application()
        self.assertEqual(str(app), '(application: "kth-azure-app", cluster: "stage")')
