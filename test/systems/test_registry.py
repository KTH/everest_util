__author__ = 'tinglev@kth.se'

import unittest
import responses
from everest_util.systems.registry import Registry, RegistryImageException, RegistryHTTPException

class GitTests(unittest.TestCase):

    def test_get_tags_url(self):
        registry = Registry('', '', 'https://test.com')
        tags_url = registry._get_tags_url('kth-azure-app')
        self.assertEqual(tags_url, 'https://test.com/v2/kth-azure-app/tags/list')

    @responses.activate
    def test_get_image_tags(self):
        registry = Registry('', '', 'https://test.com')
        responses.add(responses.GET, 'https://test.com/v2/kth-azure-app/tags/list',
                      json=[], status=200)
        responses.add(responses.GET, 'https://test.com/v2/kth-azure-app/tags/list',
                      json={'name': 'kth-azure-app', 'tags':
                            ['2.4.184_bd355c4', '2.4.186_599e682', '2.5.16_6b45aba']}, status=200)
        responses.add(responses.GET, 'https://test.com/v2/kth-azure-app/tags/list',
                      json=[], status=500)
        self.assertRaises(RegistryImageException, registry.get_image_tags, 'kth-azure-app')
        tags = registry.get_image_tags('kth-azure-app')
        self.assertEqual(tags, ['2.4.184_bd355c4', '2.4.186_599e682', '2.5.16_6b45aba'])
        self.assertRaises(RegistryHTTPException, registry.get_image_tags, 'kth-azure-app')
