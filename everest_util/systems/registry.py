"""
Module to handle docker registry requests
"""
__author__ = 'tinglev@kth.se'

import logging
import requests
from requests import ConnectionError, HTTPError, Timeout
from everest_util.base_exception import EverestException

class RegistryImageException(EverestException):
    """
    Exception raised when there was a trouble with a specific image, such as
    missing tags.
    """
    pass

class RegistryHTTPException(EverestException):
    """
    Exception raised when an http error of some sort occurs during connection
    to the registry
    """
    pass

class Registry(object):
    """
    The registry class
    """

    def __init__(self, username, password, base_url):
        """
        Constructor

        Args:
            username: username to login to the registry with
            password: password to login to the registry with
            base_url: the base url for the registry (example: https://private-registry.domain.com)
        """
        self.username = username
        self.password = password
        self.base_url = base_url
        self.log = logging.getLogger(__name__)
        # Suppress "Starting new HTTPS connection (1)" logging from requests.
        logging.getLogger("requests").setLevel(logging.WARNING)

    def get_image_tags(self, image_name):
        """
        Gets the tags for the given image name from the registry

        Args:
            image_name: the name of the image

        Returns:
            json array: an array with all tags for the given image

        Raises:
            RegistryImageException: on no tags found or parse error of tags
        """
        self.log.debug('Getting tags for image "%s"', image_name)
        url = self._get_tags_url(image_name)
        response = self._registry_request(url)
        return self._get_tags_list_from_response(response)

    def _get_tags_list_from_response(self, response):
        try:
            return response.json()['tags']
        except (KeyError, TypeError) as key_err:
            raise RegistryImageException('Docker registry did not return any tags', key_err)
        except ValueError as json_err:
            raise RegistryImageException('Could not parse json response from registry', json_err)

    def _get_tags_url(self, image_name):
        tags_url = "{}/v2/{}/tags/list".format(self.base_url, image_name)
        self.log.debug('Getting tags from url %s', tags_url)
        return tags_url

    def _registry_request(self, url):
        try:
            response = requests.get(url, auth=(self.username, self.password))
            response.raise_for_status()
            return response
        except Timeout as timeout_ex:
            raise RegistryHTTPException('Request to Docker registry timed out', ex=timeout_ex)
        except ConnectionError as conn_ex:
            raise RegistryHTTPException('Connection error from Docker registry', ex=conn_ex)
        except HTTPError as http_ex:
            self._handle_http_error(http_ex, url)

    def _handle_http_error(self, error, url):
        code = error.response.status_code
        if code == 404:
            raise RegistryImageException('Nothing found in Docker registry for {}'
                                         .format(url), ex=error)
        else:
            raise RegistryHTTPException('Docker registry returned status code {} for {}'
                                        .format(code, url), ex=error)
