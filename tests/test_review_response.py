from unittest import TestCase
from unittest.mock import patch

from plugins.review_plugin import review
from faker import fake_creds, FakeClient, FakeMessage
from common.utils import render


class TestReview(TestCase):
    client = FakeClient()

    wrong_msg = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'rate abc'
    }

    invalid_rating_msg0 = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'rate abc1 0'
    }

    invalid_rating_msg6 = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'rate abc1 6'
    }

    invalid_rating_msg_string = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'rate abc1 good'
    }

    valid_rating_msg = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'rate 7dj9u8e 5 good food',
        'user': 'anonymous'
    }

    wrong_msg_format = FakeMessage(client, wrong_msg)
    invalid_rating_value0 = FakeMessage(client, invalid_rating_msg0)
    invalid_rating_value6 = FakeMessage(client, invalid_rating_msg6)
    invalid_rating_value_str = FakeMessage(client, invalid_rating_msg_string)
    valid_rating = FakeMessage(client, valid_rating_msg)

    @patch('slackbot.dispatcher.Message', return_value=wrong_msg_format)
    def test_wrong_rating_format(self, mock_msg):
        mock_msg.body = self.wrong_msg
        review(mock_msg)
        error = 'You entered a wrong rating format.'

        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('review_response.j2', error=error)
        )

    @patch('slackbot.dispatcher.Message', return_value=invalid_rating_value0)
    def test_valid_rating_value_less_than_1(self, mock_msg):
        mock_msg.body = self.invalid_rating_msg0
        review(mock_msg)
        error = 'Invalid rating value.'

        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('review_response.j2', error=error)
        )

    @patch('slackbot.dispatcher.Message', return_value=invalid_rating_value6)
    def test_valid_rating_value_greater_than_5(self, mock_msg):
        mock_msg.body = self.invalid_rating_msg6
        review(mock_msg)
        error = 'Invalid rating value.'

        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('review_response.j2', error=error)
        )

    @patch('plugins.review_plugin.ReviewHelper.make_api_request_for_review')
    @patch('slackbot.dispatcher.Message', return_value=valid_rating_msg)
    def test_duplicate_user_rating(self, mock_msg, api_mock):
        mock_msg.body = self.valid_rating_msg
        api_mock.return_value = 'duplicate'
        context = {
            'duplicate': True
        }

        review(mock_msg)
        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('review_response.j2', context=context)
        )

    @patch('plugins.review_plugin.ReviewHelper.make_api_request_for_review')
    @patch('slackbot.dispatcher.Message', return_value=invalid_rating_value_str)
    def test_invalid_number_for_rating(self, mock_msg, api_mock):
        mock_msg.body = self.invalid_rating_msg_string
        review(mock_msg)
        error = 'good is not a valid number'

        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('review_response.j2', error=error)
        )

    @patch('plugins.review_plugin.ReviewHelper.make_api_request_for_review')
    @patch('slackbot.dispatcher.Message', return_value=valid_rating_msg)
    def test_valid_user_rating(self, mock_msg, api_mock):
        mock_msg.body = self.valid_rating_msg
        api_mock.return_value = 'success'
        context = {
            'success': True
        }

        review(mock_msg)
        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('review_response.j2', context=context)
        )

    @patch('plugins.review_plugin.ReviewHelper.make_api_request_for_review')
    @patch('slackbot.dispatcher.Message', return_value=valid_rating_msg)
    def test_invalid_serving_id_rating(self, mock_msg, api_mock):
        mock_msg.body = self.valid_rating_msg
        api_mock.return_value = None
        error = 'Invalid menu id.'

        review(mock_msg)
        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('review_response.j2', error=error)
        )
