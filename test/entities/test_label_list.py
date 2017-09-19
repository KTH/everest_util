__author__ = 'tinglev@kth.se'

import unittest
import json
from mock import patch
from everest_util.entities.label_list import LabelList
from everest_util.json_encoder import ApplicationJsonEncoder

class LabelListTests(unittest.TestCase):

    def test_add_label(self):
        label_list = LabelList()
        label_list.add_label('_label', '_value')
        self.assertEqual(label_list._label_list[0], {'label': '_label', 'value': '_value'})

    def test_to_json(self):
        label_list = LabelList()
        label_list.add_label('_label', '_value')
        label_list.add_label('_label2', '_value2')
        expected = [{'label': '_label', 'value': '_value'}, {'label': '_label2', 'value': '_value2'}]
        self.assertEqual(json.loads(json.dumps(label_list, cls=ApplicationJsonEncoder)), expected)

    def test_deserialize(self):
        label_list1 = LabelList()
        label_list1.add_label('_label', '_value')
        label_list1.add_label('_label2', '_value2')
        label_list2 = LabelList().deserialize(json.dumps(label_list1, cls=ApplicationJsonEncoder))
        self.assertEqual(label_list1, label_list2)