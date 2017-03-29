from unittest import mock, TestCase

from plugins import help_plugin
from faker import FAKE_CHANNEL, FakeClient, FakeMessage
from common.utils import render


class TestHelpFunction(TestCase):

    def message():
        client = FakeClient()
        msg = {
            'channel': FAKE_CHANNEL,
            'type': 'message',
            'text': 'help'
        }

        return FakeMessage(client, msg)

    @mock.patch('slackbot.dispatcher.Message', return_value=message)
    def test_help(self, mock_object):
        help_plugin.help(mock_object)

        self.assertTrue(mock_object.reply.called)
        mock_object.reply.assert_called_with(render('help_response.j2'))
