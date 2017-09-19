__author__ = 'tinglev@kth.se'

import unittest
import json
from mock import patch
from everest_util.entities.image import Image
from everest_util.entities.application import ApplicationJsonEncoder

class ImageTests(unittest.TestCase):

    def test_deserialize(self):
        image1 = Image()
        image1.set_name('kth-azure-app')
        image1.set_static_version('1.0')
        image1.set_semver_version('~2.0')
        json_string = json.dumps(image1.default())
        image2 = Image()
        image2.deserialize(json_string)
        self.assertEqual(image1, image2)
