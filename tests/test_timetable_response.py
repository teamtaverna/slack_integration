from unittest import TestCase
from unittest.mock import patch

from plugins import timetable_plugin
from faker import fake_creds, FakeClient, FakeMessage
from common.utils import render


class TestTimetableFunction(TestCase):

    client = FakeClient()
    msg = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'show timetable'
    }

    fake_message = FakeMessage(client, msg)

    @patch('slackbot.dispatcher.Message', return_value=fake_message)
    @patch('common.utils.make_api_request_for_timetables')
    def test_timetable(self, utils_mock, mock_msg_object):
        utils_mock.return_value = [{'slug': 'timetable1'}]
        context = {
            'timetable_names': [utils_mock.return_value[0]['slug']]
        }
        mock_msg_object.body = self.msg
        timetable_plugin.timetable(mock_msg_object)

        self.assertTrue(mock_msg_object.reply.called)

        mock_msg_object.reply.assert_called_with(
            render('timetable_response.j2', context)
        )
