"""
Module for interfacing with the subprocess library
"""

__author__ = 'tinglev@kth.se'

import subprocess
import logging

class ProcessException(Exception):
    """
    Thrown when ever the subprocess execution fails
    """
    pass


class Process(object):
    """
    Class for subprocess calls
    """

    log = logging.getLogger(__name__)

    @staticmethod
    def run_with_output(cmd):
        """
        Calls a given command and returns its output
        Args:
            cmd: the command to run
        Returns:
            string: the output from the command run
        Raises:
            ProcessException: on error during execution
        """
        try:
            Process.log.debug('Running command with output: "%s"', cmd)
            return subprocess.check_output("{0}".format(cmd), stderr=subprocess.STDOUT,
                                           shell=True, close_fds=True)
        except subprocess.CalledProcessError as cpe:
            raise ProcessException('Shell command gave error with output "{}"'
                                  .format(cpe.output.rstrip('\n')))
