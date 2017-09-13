"""
Module for simpler Slack webhook integrations

For more information on the different fields that are used in the payload see:
https://api.slack.com/docs/messages
"""

__author__ = 'tinglev@kth.se'

import logging
import requests
from requests import HTTPError, ConnectTimeout, RequestException

class SlackHTTPErrorException(Exception):
    """
    Wrapper around requests.HTTPError
    """
    pass

class SlackTimeoutException(Exception):
    """
    Wrapper around requests.ConnectTimeout
    """
    pass

class SlackRequestException(Exception):
    """
    Wrapper around requests.RequestException
    """
    pass

class SlackTooManyAttachmentsException(Exception):
    """
    Raised when the number of attachments for a payload
    are more than 20
    """
    pass


class Slack(object):
    """
    The class
    """

    def __init__(self, webhook_url):
        """
        Constructor for the Slack class

        Args:
            webhook_url: the webhook url to use for this class instance
        """
        self.log = logging.getLogger(__name__)
        self.webhook_url = webhook_url

    def add_attachement_to_body(self, body, attachment):
        """
            Adds an attachment to a payload body object

            Args:
                body: the body of a payload object
                attachment: the attachment object to add to the body

            Returns:
                json: the body object with the attachment added

            Raises:
                SlackTooManyAttachmentsException: when the number of attachments
                    are too big
        """
        attachments_field = 'attachments'
        if not attachments_field in body:
            body[attachments_field] = []
        if len(body[attachments_field]) > 19:
            raise SlackTooManyAttachmentsException
        body[attachments_field].append(attachment)
        return body


    def create_payload_attachment(self, fallback, color, author_name, author_link, title, text):
        """
        Creates a valid Slack attachment to attach to a payload body

        Args:
            fallback: the fallback text of the message
            color: the color of the attachment
            author_name: the name of the author
            author_link: the link when clicking the authors name
            title: the title
            text: the text

        Returns:
            json: a valid Slack attachment json object
        """
        return {
            "fallback": fallback,
            "color": color,
            "author_name": author_name,
            "author_link": author_link,
            "title": title,
            "text": text
        }

    def create_payload_body(self, channel, text, username, icon):
        """
        Creates a valid Slack payload body from the given arguments

        Args:
            channel: the channel to send this message to
            text: the text of the message
            username: the username to show as the sender in Slack for this message
            icon: the emoji to use for this message (for instance :+1:)

        Returns:
            json: a valid Slack payload body json object
        """
        return {
            "channel": channel,
            "text": text,
            "username": username,
            "icon_emoji": icon
        }

    def call_slack_endpoint(self, payload):
        """
        Makes the actual REST call to the webhook url with a given payload

        Args:
            payload: a json object with the Slack payload to send

        Returns:
            response: the requests.response object returned from the call

        Raises:
            Wrapped exceptions (see above)
        """
        try:
            self.log.debug('Calling Slack with payload "%s"', payload)
            response = requests.post(self.webhook_url, json=payload)
            self.log.debug('Response was "%s"', response.text)
            return response
        except HTTPError:
            raise SlackHTTPErrorException
        except ConnectTimeout:
            raise SlackTimeoutException
        except RequestException:
            raise SlackRequestException
                        