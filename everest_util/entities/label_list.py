"""
Class representation of a list of labels from a docker-stack file
"""
__author__ = 'tinglev@kth.se'

import json
 
class LabelList(object):
    """
    The class
    """

    def __init__(self):
        """
        Constructor
        """
        self._label_list = []

    def default(self):
        """
        JSONEncoder override

        Returns:
            json: a json representation of this class
        """
        return self._label_list

    def add_label(self, label, value):
        """
        Adds a label to the list

        Args:
            label: the label
            value: the value
        """
        self._label_list.append({'label': label, 'value': value})

    def __len__(self):
        """
        Length override
        """
        return len(self._label_list)

    def __eq__(self, label_list):
        """
        Equality operator override
        """
        return self._label_list == label_list

    def deserialize(self, json_string):
        """
        Deserializes this object from a valid json string

        Args:
            json_string: a string containing valid json

        Returns:
            self: for chaining purposes
        """
        json_data = json.loads(json_string)
        for label in json_data:
            self.add_label(label['label'], label['value'])
        return self
