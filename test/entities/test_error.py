__author__ = 'tinglev@kth.se'

import unittest
import json
from everest_util.entities.error import Error
from everest_util.json_encoder import ApplicationJsonEncoder

class ErrorTests(unittest.TestCase):

    def test_deserialize(self):
        error1 = Error('the message', 'the stack\ntrace')
        error2 = Error().deserialize(json.dumps(error1, cls=ApplicationJsonEncoder))
        self.assertEqual(error1, error2)
