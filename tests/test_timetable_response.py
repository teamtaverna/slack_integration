from unittest import TestCase
from unittest.mock import patch

from plugins import timetable_plugin
from faker import fake_creds, FakeClient, FakeMessage
from common.utils import render


class TestTimetableFunction(TestCase):

    client = FakeClient()

    correct_msg = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'show timetable'
    }

    correct_msg_spaces = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'show     timetable'
    }

    wrong_msg = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'show timetables'
    }

    correct_message = FakeMessage(client, correct_msg)
    wrong_message = FakeMessage(client, wrong_msg)
    correct_msg_with_spaces = FakeMessage(client, correct_msg_spaces)

    @patch('slackbot.dispatcher.Message', return_value=correct_message)
    @patch('common.utils.make_api_request_for_timetables')
    def test_timetable_with_correct_message(self, utils_mock, mock_msg):
        utils_mock.return_value = [{'slug': 'timetable1'}]
        context = {
            'timetable_names': [utils_mock.return_value[0]['slug']]
        }
        mock_msg.body = self.correct_msg
        timetable_plugin.timetable(mock_msg)

        self.assertTrue(mock_msg.reply.called)

        mock_msg.reply.assert_called_with(
            render('timetable_response.j2', context)
        )

    @patch('slackbot.dispatcher.Message', return_value=correct_msg_with_spaces)
    @patch('common.utils.make_api_request_for_timetables')
    def test_timetable_with_spaces_in_correct_msg(self, utils_mock, mock_msg):
        utils_mock.return_value = [{'slug': 'timetable1'}]
        context = {
            'timetable_names': [utils_mock.return_value[0]['slug']]
        }
        mock_msg.body = self.correct_msg_spaces
        timetable_plugin.timetable(mock_msg)

        self.assertTrue(mock_msg.reply.called)

        mock_msg.reply.assert_called_with(
            render('timetable_response.j2', context)
        )

    @patch('slackbot.dispatcher.Message', return_value=wrong_message)
    @patch('common.utils.make_api_request_for_timetables')
    def test_timetable_with_wrong_message(self, utils_mock, mock_msg):
        utils_mock.return_value = [{'slug': 'timetable1'}]

        mock_msg.body = self.wrong_msg
        timetable_plugin.timetable(mock_msg)

        self.assertTrue(mock_msg.reply.called)

        mock_msg.reply.assert_called_with(
            render('help_response.j2')
        )

    @patch('slackbot.dispatcher.Message', return_value=correct_message)
    @patch('common.utils.make_api_request_for_timetables')
    def test_timetable_with_with_empty_db(self, utils_mock, mock_msg):
        utils_mock.return_value = []
        context = {
            'timetable_names': []
        }
        mock_msg.body = self.correct_msg
        timetable_plugin.timetable(mock_msg)

        self.assertTrue(mock_msg.reply.called)

        mock_msg.reply.assert_called_with(
            render('timetable_response.j2', context)
        )
