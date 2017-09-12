"""
Class representation of a list of labels from a docker-stack file
"""
__author__ = 'tinglev@kth.se'

class LabelList(object):
    """
    The class
    """

    def __init__(self):
        """
        Constructor
        """
        self._label_list = []

    def to_json(self):
        """
        Returns a JSON representation of the label list
        Returns:
            json array: a JSON array of object on the format [{label: 'label', value: 'value'}]
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
