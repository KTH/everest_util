__author__ = 'tinglev@kth.se'

import json

class ApplicationJsonEncoder(json.JSONEncoder):
    def default(self, o): # pylint: disable=E0202
        if hasattr(o, 'default'):
            return o.default()
        else:
            return json.JSONEncoder.default(self, o)