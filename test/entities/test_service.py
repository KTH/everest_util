__author__ = 'tinglev'

import unittest
import json
from mock import patch, MagicMock
from everest_util.entities.service import Service, ServiceException
from everest_util.entities.application import ApplicationJsonEncoder
from everest_util.entities.image import Image
from everest_util.entities.label_list import LabelList
from everest_util.systems.registry import Registry

class ServiceTests(unittest.TestCase):

    def test_parse_image_registry(self):
        service = Service(Registry('', '', ''))
        service._parse_image_registry('kthregistryv2.sys.kth.se/kth-azure-app:1.0.0_abc')
        self.assertEqual(service._image.get_registry(), 'kthregistryv2.sys.kth.se')
        service._parse_image_registry('redis:1.0.0_abc')
        self.assertIsNone(service._image.get_registry())

    def test_parse_image_name(self):
        service = Service(Registry('', '', ''))
        service._parse_image_name('kthregistryv2.sys.kth.se/kth-azure-app:1.0.0_abc')
        self.assertEqual(service._image.get_name(), 'kth-azure-app')
        service._parse_image_name('redis:1.0.0_abc')
        self.assertEqual(service._image.get_name(), 'redis')
        self.assertRaises(ServiceException, service._parse_image_name, 'redis1.0.0_abc')

    def test_parse_image_version(self):
        service = Service(Registry('', '', ''))
        service._parse_image_version('kthregistryv2.sys.kth.se/kth-azure-app:1.0.0_abc')
        self.assertEqual(service._image.get_static_version(), '1.0.0_abc')
        service._parse_image_version('kth-azure-app:${{WEB_VERSION}}')
        self.assertEqual(service._image.get_static_version(), '${{WEB_VERSION}}')

    def test_parse_image_info(self):
        service = Service(Registry('', '', ''))
        service._service_struct = {}
        self.assertRaises(ServiceException, service._parse_image_info)

    def test_parse_semver_version(self):
        service = Service(Registry('', '', ''))
        service._image.set_static_version('1.0.0_abc')
        service._parse_semver_version()
        self.assertFalse(service._image.get_is_semver())
        self.assertIsNone(service._image.get_version_env_key())
        service._image.set_static_version('${WEB_VERSION}')
        service._parse_semver_version()
        self.assertTrue(service._image.get_is_semver())
        self.assertEqual(service._image.get_version_env_key(), 'WEB_VERSION')

    def test_get_env_value_from_struct(self):
        service = Service(Registry('', '', ''))
        service._service_struct = {'environment': {'WEB_VERSION': '2.0.0'}}
        result = service._get_env_value_from_struct('WEB_VERSION')
        self.assertEqual(result, '2.0.0')
        self.assertRaises(ServiceException, service._get_env_value_from_struct, 'NOPE')
        del service._service_struct['environment']
        self.assertRaises(ServiceException, service._get_env_value_from_struct, 'WEB_VERSION')

    def test_is_valid_label(self):
        service = Service(Registry('', '', ''))
        self.assertTrue(service._is_valid_label('TEST=TEST'))
        self.assertTrue(service._is_valid_label('TEST3_VAR=TEST3_VAL'))
        self.assertTrue(service._is_valid_label('TEST="Test with space"'))
        self.assertFalse(service._is_valid_label('#TEST=TEST'))
        self.assertFalse(service._is_valid_label('"Test with space"=TEST'))
        self.assertFalse(service._is_valid_label('TEST==TEST'))
        self.assertFalse(service._is_valid_label('TEST="TEST'))
        self.assertFalse(service._is_valid_label('TEST=TEST SPACE'))
        self.assertTrue(service._is_valid_label('com.df.notify=true'))

    def test_parse_labels(self):
        service = Service(Registry('', '', ''))
        service.log.debug = MagicMock()
        service._service_struct = {'labels': ['LABEL1=VALUE1', 'LABEL2=VALUE2']}
        service._parse_labels()
        self.assertEqual(service._labels._label_list[0], {'label': 'LABEL1', 'value': 'VALUE1'})
        self.assertEqual(service._labels._label_list[1], {'label': 'LABEL2', 'value': 'VALUE2'})
        service._service_struct = {'labels': []}
        service._labels = LabelList()
        service._parse_labels()
        self.assertEqual(service._labels._label_list, [])
        service._service_struct = {'labels': ['LABEL1=VALUE1', '#LABEL2=VALUE2']}
        service._labels = LabelList()
        service._parse_labels()
        self.assertEqual(service._labels._label_list[0], {'label': 'LABEL1', 'value': 'VALUE1'})
        self.assertEqual(len(service._labels._label_list), 1)
        del service._service_struct['labels']
        self.assertRaises(ServiceException, service._parse_labels)

    def test_parse_deploy_labels(self):
        service = Service(Registry('', '', ''))
        service.log.debug = MagicMock()
        service._service_struct = {'deploy': {'labels': ['LABEL1=VALUE1', 'LABEL2=VALUE2']}}
        service._parse_deploy_labels()
        self.assertEqual(service._deploy_labels._label_list[0], {'label': 'LABEL1', 'value': 'VALUE1'})
        self.assertEqual(service._deploy_labels._label_list[1], {'label': 'LABEL2', 'value': 'VALUE2'})
        service._service_struct = {'deploy': {'labels': []}}
        service._deploy_labels = LabelList()
        service._parse_deploy_labels()
        self.assertEqual(service._deploy_labels._label_list, [])
        service._service_struct = {'deploy': {'labels': ['LABEL1=VALUE1', '#LABEL2=VALUE2']}}
        service._deploy_labels = LabelList()
        service._parse_deploy_labels()
        self.assertEqual(service._deploy_labels._label_list[0], {'label': 'LABEL1', 'value': 'VALUE1'})
        self.assertEqual(len(service._deploy_labels._label_list), 1)
        del service._service_struct['deploy']
        self.assertRaises(ServiceException, service._parse_deploy_labels)

    def test_to_json(self):
        service = Service(Registry('', '', ''))
        service._name = 'web'
        service._labels.add_label('label1', 'value1')
        service._labels.add_label('label2', 'value2')
        service._deploy_labels.add_label('d_label1', 'value1')
        service._deploy_labels.add_label('d_label2', 'value2')
        service._env_list.add_env('ENV_1', 'VAL_1')
        service._image = Image()
        service._image.set_name('kth-azure-app')
        service._image.set_static_version('1.0')
        service._image.set_semver_version('2.0')
        expected =  {'service_name': 'web', 'environment': [{'key': 'ENV_1', 'value': 'VAL_1'}],
                     'labels': [{'label': 'label1', 'value': 'value1'}, {'label': 'label2', 'value': 'value2'}],
                     'deploy_labels': [{'label': 'd_label1', 'value': 'value1'}, {'label': 'd_label2', 'value': 'value2'}],
                     'image': {'image_name': 'kth-azure-app', 'static_version': '1.0', 'semver_version': '2.0'}}
        self.assertEqual(json.loads(json.dumps(service, cls=ApplicationJsonEncoder)), expected)

    def test_get_resources(self):
        service = Service(Registry('', '', ''))
        service._service_struct = {'deploy': {'resources': {'limits': {'cpus': '0.001',
                                                                       'memory': '50M'}}}}
        result = service.get_resources()
        self.assertEqual(result['limits']['cpus'], '0.001')
        self.assertNotIn('reservations', result)
        del service._service_struct['deploy']['resources']
        self.assertRaises(KeyError, service.get_resources)

    def test_get_restart_policy(self):
        service = Service(Registry('', '', ''))
        service._service_struct = {'deploy': {'restart_policy':
                                    {'condition': 'on-failure',
                                     'max-attempts': '2',
                                     'delay': '5s',
                                     'window': '30s'}}}
        result = service.get_restart_policy()
        self.assertEqual(result['condition'], 'on-failure')
        del service._service_struct['deploy']['restart_policy']
        self.assertRaises(KeyError, service.get_restart_policy)

    def test_get_logging_policy(self):
        service = Service(Registry('', '', ''))
        service._service_struct = {'logging': {'options':
                                    {'max-file': '5',
                                     'max-size': '10m'}}}
        result = service.get_logging_policy()
        self.assertEqual(result['options']['max-file'], '5')
        del service._service_struct['logging']
        self.assertRaises(KeyError, service.get_logging_policy)

class ImageTests(unittest.TestCase):

    def test_equal(self):
        img1 = Image()
        img1.set_name('web')
        img1.set_static_version('1.0')
        img1.set_semver_version('2.0')
        img2 = Image()
        img2.set_name('web')
        img2.set_static_version('1.0')
        img2.set_semver_version('2.0')
        self.assertEqual(img1, img2)
        img2.set_name('redis')
        self.assertNotEqual(img1, img2)
        img2.set_name('web')
        img2.set_static_version('1.0.1')
        self.assertNotEqual(img1, img2)
        img2.set_static_version('1.0')
        img2.set_semver_version('1.0')
        self.assertNotEqual(img1, img2)
        img2.set_semver_version('2.0')
        img2.set_is_semver(True)
        self.assertEqual(img1, img2)

    def test_to_json(self):
        img = Image()
        img.set_name('web')
        img.set_static_version('1.0')
        img.set_semver_version('2.0')
        expected = {'image_name': 'web', 'static_version': '1.0', 'semver_version': '2.0'}
        self.assertEqual(json.loads(json.dumps(img, cls=ApplicationJsonEncoder)), expected)
