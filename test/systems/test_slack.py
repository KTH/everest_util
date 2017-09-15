__author__ = 'tinglev@kth.se'

import unittest
import responses
from everest_util.systems.slack import Slack, SlackHTTPErrorException

class SlackTests(unittest.TestCase):

    def test_create_payload_body(self):
        slack = Slack('https://test.com/webhook')
        body = slack.create_payload_body('#channel', 'text here', 'username', ':+1:')
        expected = {'channel': '#channel', 'text': 'text here', 'username': 'username',
                    'icon_emoji': ':+1:'}
        self.assertEqual(body, expected)

    def test_create_payload_attachment(self):
        slack = Slack('https://test.com/webhook')
        attachment = slack.create_payload_attachment('fallback', '#aabbcc', 'tinglev',
                                                     'https://www.kth.se', 'a title', 'some text')
        expected = {'fallback': 'fallback', 'color': '#aabbcc', 'author_name': 'tinglev',
                    'author_link': 'https://www.kth.se', 'title': 'a title', 'text': 'some text'}
        self.assertEqual(attachment, expected)

    def test_add_attachment_to_body(self):
        slack = Slack('https://test.com/webhook')
        body = slack.create_payload_body('#channel', 'text here', 'username', ':+1:')
        attachment = slack.create_payload_attachment('fallback', '#aabbcc', 'tinglev',
                                                     'https://www.kth.se', 'a title', 'some text')
        body = slack.add_attachement_to_body(body, attachment)
        self.assertEqual(body['attachments'][0]['author_name'], 'tinglev')

    @responses.activate
    def test_call_slack_endpoint(self):
        slack = Slack('https://test.com/webhook')
        responses.add(responses.POST, 'https://test.com/webhook',
                      json={}, status=200)
        responses.add(responses.POST, 'https://test.com/webhook',
                      json={}, status=404)
        self.assertEqual(slack.call_slack_endpoint({'payload': 'payload'}).status_code, 200)
        self.assertRaises(SlackHTTPErrorException, slack.call_slack_endpoint,
                          {'payload': 'payload'})
