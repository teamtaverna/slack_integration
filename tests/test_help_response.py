from unittest import mock, TestCase

from plugins import help_plugin

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


class TestHelpFunction(TestCase):
    client = FakeClient()
    msg = {
        'channel': FAKE_CHANNEL,
        'type': 'message',
        'text': 'help'
    }

    message = FakeMessage(client, msg)

    @mock.patch('slackbot.dispatcher.Message', return_value=message)
    def test_help(self, mock_object):
        help_plugin.help(mock_object)

        self.assertTrue(mock_object.reply.called)
