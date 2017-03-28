import unittest
from plugins import help_plugin
from unittest import mock

FAKE_BOT_ID = 'US99999'
FAKE_BOT_ATNAME = '<@' + FAKE_BOT_ID + '>'
FAKE_CHANNEL = 'C12942JF92'

class FakeClient:
    def __init__(self):
        self.rtm_messages = []

    def rtm_send_message(self, channel, message, attachments=None):
        self.rtm_messages.append((channel, message))

class FakeMessage:
    def __init__(self, client, msg):
        self._client = client
        self._msg = msg

    def reply(self, message):
        # Perhaps a bit unnecessary to do it this way, but it's close to how
        # dispatcher and message actually works
        self._client.rtm_send_message(self._msg['channel'], message)
#
class TestHelpFunction(unittest.TestCase):
    client = FakeClient()
    msg = {
        'text': FAKE_BOT_ATNAME + ' hello',
        'channel': 'G99999'
    }

    message = FakeMessage(client, msg)


    @mock.patch('slackbot.dispatcher.Message', return_value=message)
    def test_help(self, mock_message):
        self.assertIn('Help', help_plugin.help(mock_message))
