from unittest import mock, TestCase

from plugins import help_plugin
from faker import fake_creds, FakeClient, FakeMessage


class TestHelpFunction(TestCase):
    client = FakeClient()
    msg = {
        'channel': fake_creds()['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'help'
    }

    message = FakeMessage(client, msg)

    @mock.patch('slackbot.dispatcher.Message', return_value=message)
    def test_help(self, mock_object):
        help_plugin.help(mock_object)

        self.assertTrue(mock_object.reply.called)
