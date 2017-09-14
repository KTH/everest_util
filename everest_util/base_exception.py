"""
Base exceptions for all exceptions defined in this library
"""
__author__ = 'tinglev@kth.se'

class EverestException(Exception):
    """
    The class
    """

    def __init__(self, message, ex=None):
        """
        Constructor that allows the original exception to be appended, if requested
        """
        if ex:
            message = '{} ({})'.format(message, ex.message)
        super(EverestException, self).__init__(message)
