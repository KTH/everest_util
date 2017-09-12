"""
Module to handle docker registry requests
"""
__author__ = 'tinglev@kth.se'

import logging
import requests
from requests import ConnectionError, HTTPError, Timeout

class RegistryImageException(Exception):
    """
    Exception raised when there was a trouble with a specific image, such as
    missing tags.
    """
    pass

class RegistryHTTPException(Exception):
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
        """
        Parses a registry response for the image tags array
        Args:
            response: the requests library response for the API call to the registry
        Returns:
            json array: an array with all tags for the given image
        Raises:
            RegistryImageException: on no tags found or parse error of tags
        """
        try:
            return response.json()["tags"]
        except KeyError as key_err:
            raise RegistryImageException('KTH Docker Registry did not return any tags', key_err)
        except ValueError as json_err:
            raise RegistryImageException('Could not parse json response from registry', json_err)

    def _get_tags_url(self, image_name):
        """
        Constructs a list tags API call url for an image name
        Args:
            image_name: the name of the image
        Returns:
            string: the url for the API call
        """
        tags_url = "{}/v2/{}/tags/list".format(self.base_url, image_name)
        self.log.debug('Getting tags from url %s', tags_url)
        return tags_url

    def _registry_request(self, url):
        """
        Makes the actual request to the registry API
        Args:
            url: the url to request
        Returns:
            requests->response: a response object for the call
        Raises
            RegistryHTTPException: on timeout, connection error or other http error
            RegistryImageException: on a 404 response from the registry, indicating that
                                    the given image has no tags
        """
        try:
            response = requests.get(url, auth=(self.username, self.password))
            response.raise_for_status()
            return response
        except Timeout as timeout_ex:
            raise RegistryHTTPException('Request to KTH Docker Registry timed out', ex=timeout_ex)
        except ConnectionError as conn_ex:
            raise RegistryHTTPException('Connection error from KTH Docker Registry', ex=conn_ex)
        except HTTPError as http_ex:
            self._handle_http_error(http_ex, url)

    def _handle_http_error(self, error, url):
        """
        QoL function to handle HTTPErrors from the request
        Args:
            error: the HTTPError raised
            url: the original url called
        Returns:
            Nothing
        Raises:
            RegistryHTTPException: on a non-404 code in the response
            RegistryImageException: on a 404 response from the registry, indicating that
                                    the given image has no tags            
        """
        code = error.response.status_code
        if code == 404:
            raise RegistryImageException('Nothing found in KTH Docker Registry for {}'
                                         .format(url), ex=error)
        else:
            raise RegistryHTTPException('KTH Docker Registry returned status code {} for {}'
                                        .format(code, url), ex=error)
