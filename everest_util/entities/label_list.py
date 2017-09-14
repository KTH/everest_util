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
