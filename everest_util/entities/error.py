"""
Class representation of an error
"""
__author__ = 'tinglev@kth.se'

import json

class Error(object):
    """
    The class
    """

    def __init__(self, message=None, stack_trace=None):
        self.message = message
        self.stack_trace = stack_trace

    def __eq__(self, error):
        """
        Equality operator override
        """
        return (self.message == error.message and
                self.stack_trace == error.stack_trace)

    def default(self):
        """
        JSONEncoder override

        Returns:
            json: a json representation of this class
        """
        return dict(message=self.message,
                    stack_trace=self.stack_trace)


    def deserialize(self, json_string):
        """
        Deserializes this object from a valid json string

        Args:
            json_string: a string containing valid json

        Returns:
            self: for chaining purposes
        """
        json_data = json.loads(json_string)
        self.message = json_data['message']
        self.stack_trace = json_data['stack_trace']
        return self
