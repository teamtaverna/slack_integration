from unittest import TestCase
from unittest.mock import patch

from plugins import help_plugin
from faker import fake_creds, FakeClient, FakeMessage
from common.utils import render


class TestHelpFunction(TestCase):

    client = FakeClient()
    msg = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'help'
    }

    fake_message = FakeMessage(client, msg)

    @patch('slackbot.dispatcher.Message', return_value=fake_message)
    def test_help(self, mock_object):
        mock_object.body = self.msg
        help_plugin.help(mock_object)

        self.assertTrue(mock_object.reply.called)
        mock_object.reply.assert_called_with(render('help_response.j2'))
