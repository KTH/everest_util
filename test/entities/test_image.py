__author__ = 'tinglev@kth.se'

import unittest
import json
from everest_util.entities.image import Image
from everest_util.json_encoder import ApplicationJsonEncoder

class ImageTests(unittest.TestCase):

    def test_deserialize(self):
        image1 = Image()
        image1.set_name('kth-azure-app')
        image1.set_static_version('1.0')
        image1.set_semver_version('~2.0')
        image2 = Image().deserialize(json.dumps(image1, cls=ApplicationJsonEncoder))
        self.assertEqual(image1, image2)
