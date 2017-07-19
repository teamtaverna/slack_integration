from unittest import TestCase
from unittest.mock import patch

from freezegun import freeze_time

from plugins.menu_plugin import MenuHelper, menu
from faker import fake_creds, FakeClient, FakeMessage
from common.utils import render, DateHelper


def servings():
    return [
        {
            'publicId': 'zaba4r4z',
            'dateServed': '2017-07-06',
            'vendor': {'name': 'vendor1'},
            'menuItem': {
                'cycleDay': 1,
                'meal': {'name': 'breakfast'},
                'course': {'name': 'appetizer', 'sequenceOrder': 2},
                'dish': {'name': 'bread'},
                'timetable': {'name': 'timetable1'}
            }
        },
        {
            'publicId': 'vl9l8b8w',
            'dateServed': '2017-07-06',
            'vendor': {'name': 'vendor1'},
            'menuItem': {
                'cycleDay': 1,
                'meal': {'name': 'breakfast'},
                'course': {'name': 'main dish', 'sequenceOrder': 1},
                'dish': {'name': 'rice'},
                'timetable': {'name': 'timetable1'}
            }
        },
        {
            'publicId': 'qrpr737y',
            'dateServed': '2017-07-06',
            'vendor': {'name': 'vendor1'},
            'menuItem': {
                'cycleDay': 1,
                'meal': {'name': 'lunch'},
                'course': {'name': 'main dish', 'sequenceOrder': 1},
                'dish': {'name': 'beans'},
                'timetable': {'name': 'timetable1'}
            }
        }
    ]


def sorted_servings():
    return {
        'breakfast': [
            {
                'public_id': 'vl9l8b8w',
                'course': 'main dish',
                'sequence_order': 1,
                'dish': 'rice'
            },
            {
                'public_id': 'zaba4r4z',
                'course': 'appetizer',
                'sequence_order': 2,
                'dish': 'bread'
            }
        ],
        'lunch': [
            {
                'public_id': 'qrpr737y',
                'course': 'main dish',
                'sequence_order': 1,
                'dish': 'beans'
            }
        ]
    }


class MenuHelperTest(TestCase):
    """Tests the MenuHelper class."""

    servings = servings()

    def setUp(self):
        self.menu_helper = MenuHelper()
        self.sorted_servings = sorted_servings()

    def test_servings_to_dict(self):
        servings_to_dict = self.menu_helper.servings_to_dict(self.servings)

        self.assertEqual(servings_to_dict, self.sorted_servings)

    @patch('plugins.menu_plugin.MenuHelper.make_api_request_for_servings')
    def test_get_meals(self, mock_obj):
        mock_obj.return_value = self.servings
        meals = self.menu_helper.get_meals('timetable1', 'today')

        self.assertEqual(meals, self.sorted_servings)

    @patch('plugins.menu_plugin.MenuHelper.make_api_request_for_servings')
    def test_get_meals_without_servings(self, mock_obj):
        mock_obj.return_value = None
        meals = self.menu_helper.get_meals('timetable1', 'today')

        self.assertEqual(meals, None)

    @freeze_time('2017-07-06')
    @patch('common.utils.DateHelper.date_to_str', return_value='2017-07-06')
    @patch('plugins.menu_plugin.MenuHelper.make_api_request_for_events')
    def test_past_events(self, mock_event, day_mock):
        event_list = [
            {
                'name': 'event1',
                'action': 'NO_MEAL',
                'startDate': '2017-07-01T08:00:00+00:00',
                'endDate': '2017-07-03T00:00:00+00:00'
            }
        ]
        mock_event.return_value = event_list
        events = self.menu_helper.get_event('today')

        self.assertEqual(events, [])

    @freeze_time('2017-07-06')
    @patch('plugins.menu_plugin.MenuHelper.make_api_request_for_events')
    def test_present_events(self, mock_event):
        event_list = [
            {
                'name': 'event1',
                'action': 'NO_MEAL',
                'startDate': '2017-07-04T08:00:00+00:00',
                'endDate': '2017-07-07T00:00:00+00:00'
            }
        ]
        mock_event.return_value = event_list
        events = self.menu_helper.get_event('today')

        self.assertEqual(events, event_list)

    @freeze_time('2017-07-06')
    @patch('plugins.menu_plugin.MenuHelper.make_api_request_for_events')
    def test_no_event(self, mock_event):
        mock_event.return_value = []
        events = self.menu_helper.get_event('today')

        self.assertEqual(events, [])

    @freeze_time('2017-07-06')
    @patch('plugins.menu_plugin.MenuHelper.get_event', return_value=['random'])
    def test_meals_check_context_update_with_events(self, mock_obj):
        meals = self.sorted_servings
        context = {'random': 'stuff'}
        self.menu_helper.meals_check_context_update(
            meals, context, 'today'
        )

        updated_context = {
            'random': 'stuff',
            'no_meals': True
        }
        self.assertEqual(context, updated_context)

    @freeze_time('2017-07-06')
    @patch('plugins.menu_plugin.MenuHelper.get_event', return_value=[])
    def test_meals_check_context_update_without_events(self, mock_obj):
        meals = self.sorted_servings
        context = {'random': 'stuff'}
        self.menu_helper.meals_check_context_update(
            meals, context, 'today'
        )

        updated_context = {
            'random': 'stuff',
            'meals': meals
        }
        self.assertEqual(context, updated_context)

    def test_timetable_check_context_update_with_no_timetable(self):
        context = {'random': 'stuff'}
        response = self.menu_helper.timetable_check_context_update(
            0, 'timetable1', context
        )
        updated_context = {
            'random': 'stuff',
            'no_timetable': True
        }
        expected = render('menu_response.j2', updated_context)
        self.assertEqual(response, expected)

    def test_timetable_check_context_update_with_available_timetable(self):
        context = {}
        response = self.menu_helper.timetable_check_context_update(
            1, 'timetable1', context
        )
        error = 'timetable1 is not a valid timetable name.'

        expected = render('timetable_response.j2', error=error)
        self.assertEqual(response, expected)


class MenuTest(TestCase):
    """Tests the menu function."""

    date_helper = DateHelper()
    client = FakeClient()
    menu = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'menu'
    }

    menu_timetable = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'menu timetable1'
    }

    menu_wrong_timetable = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'menu wrongstuff'
    }

    menu_weekday = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'menu timetable1 monday'
    }

    menu_wrong_weekday = {
        'channel': fake_creds['FAKE_CHANNEL'],
        'type': 'message',
        'text': 'menu timetable1 blablabla'
    }

    menu_msg = FakeMessage(client, menu)
    menu_timetable_msg = FakeMessage(client, menu_timetable)
    menu_wrong_timetable_msg = FakeMessage(client, menu_wrong_timetable)
    menu_weekday_msg = FakeMessage(client, menu_weekday)
    menu_wrong_weekday_msg = FakeMessage(client, menu_wrong_weekday)

    @patch('slackbot.dispatcher.Message', return_value=menu_msg)
    @patch('common.utils.TimetableAPIUtils.make_api_request_for_timetables')
    @patch('plugins.menu_plugin.MenuHelper.get_event', return_value=[])
    @patch('plugins.menu_plugin.MenuHelper.get_meals')
    def test_menu_with_one_timetable(self, meals_mock, event_mock, utils_mock, mock_msg):
        mock_msg.body = self.menu
        utils_mock.return_value = [{'slug': 'timetable1'}]
        meals_mock.return_value = sorted_servings()
        context = {
            'timetable_names': ['timetable1'],
            'day_of_week': 'today',
            'meals': meals_mock.return_value
        }
        menu(mock_msg)

        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('menu_response.j2', context)
        )

    @patch('slackbot.dispatcher.Message', return_value=menu_msg)
    @patch('common.utils.TimetableAPIUtils.make_api_request_for_timetables')
    @patch('plugins.menu_plugin.MenuHelper.get_event', return_value=[])
    @patch('plugins.menu_plugin.MenuHelper.get_meals')
    def test_menu_with_no_timetable(self, meals_mock, event_mock, utils_mock, mock_msg):
        mock_msg.body = self.menu
        utils_mock.return_value = []
        context = {
            'timetable_names': [],
            'day_of_week': 'today',
            'no_timetable': True
        }
        menu(mock_msg)

        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('menu_response.j2', context)
        )

    @patch('slackbot.dispatcher.Message', return_value=menu_msg)
    @patch('common.utils.TimetableAPIUtils.make_api_request_for_timetables')
    @patch('plugins.menu_plugin.MenuHelper.get_event', return_value=[])
    @patch('plugins.menu_plugin.MenuHelper.get_meals')
    def test_menu_with_multiple_timetable(self, meals_mock, event_mock, utils_mock, mock_msg):
        mock_msg.body = self.menu
        utils_mock.return_value = [
            {'slug': 'timetable1'},
            {'slug': 'timetable2'}
        ]
        meals_mock.return_value = sorted_servings()
        context = {
            'timetable_names': ['timetable1', 'timetable2'],
            'day_of_week': 'today',
            'multiple_timetables': True
        }
        menu(mock_msg)

        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('menu_response.j2', context)
        )

    @patch('slackbot.dispatcher.Message', return_value=menu_timetable_msg)
    @patch('common.utils.TimetableAPIUtils.make_api_request_for_timetables')
    @patch('plugins.menu_plugin.MenuHelper.get_event', return_value=[])
    @patch('plugins.menu_plugin.MenuHelper.get_meals')
    def test_menu_timetable_command(self, meals_mock, event_mock, utils_mock, mock_msg):
        mock_msg.body = self.menu_timetable
        utils_mock.return_value = [{'slug': 'timetable1'}]
        meals_mock.return_value = sorted_servings()
        context = {
            'timetable_names': ['timetable1'],
            'day_of_week': 'today',
            'meals': meals_mock.return_value
        }
        menu(mock_msg)

        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('menu_response.j2', context)
        )

    @patch('slackbot.dispatcher.Message', return_value=menu_wrong_timetable_msg)
    @patch('common.utils.TimetableAPIUtils.make_api_request_for_timetables')
    @patch('plugins.menu_plugin.MenuHelper.get_event', return_value=[])
    @patch('plugins.menu_plugin.MenuHelper.get_meals')
    def test_menu_with_wrong_timetable(self, meals_mock, event_mock, utils_mock, mock_msg):
        mock_msg.body = self.menu_wrong_timetable
        utils_mock.return_value = [{'slug': 'timetable1'}]
        error = 'wrongstuff is not a valid timetable name.'

        menu(mock_msg)

        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('timetable_response.j2', error=error)
        )

        # Test when there are no timetables available in the database
        utils_mock.return_value = []
        context = {
            'random': 'stuff',
            'no_timetable': True
        }
        menu(mock_msg)
        mock_msg.reply.assert_called_with(
            render('menu_response.j2', context)
        )

    @patch('slackbot.dispatcher.Message', return_value=menu_weekday_msg)
    @patch('common.utils.TimetableAPIUtils.make_api_request_for_timetables')
    @patch('plugins.menu_plugin.MenuHelper.get_event', return_value=[])
    @patch('plugins.menu_plugin.MenuHelper.get_meals')
    def test_menu_with_weekday(self, meals_mock, event_mock, utils_mock, mock_msg):
        mock_msg.body = self.menu_weekday
        utils_mock.return_value = [{'slug': 'timetable1'}]
        meals_mock.return_value = sorted_servings()
        context = {
            'timetable_names': ['timetable1'],
            'day_of_week': 'monday',
            'meals': meals_mock.return_value
        }
        menu(mock_msg)

        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('menu_response.j2', context)
        )

    @patch('slackbot.dispatcher.Message', return_value=menu_wrong_weekday_msg)
    @patch('common.utils.TimetableAPIUtils.make_api_request_for_timetables')
    @patch('plugins.menu_plugin.MenuHelper.get_event', return_value=[])
    @patch('plugins.menu_plugin.MenuHelper.get_meals')
    def test_menu_with_wrong_weekday(self, meals_mock, event_mock, utils_mock, mock_msg):
        mock_msg.body = self.menu_wrong_weekday
        utils_mock.return_value = [{'slug': 'timetable1'}]
        meals_mock.return_value = sorted_servings()
        error = 'You did not enter a valid day.'
        context = {
            'random': 'stuff',
            'invalid_day': True,
            'days': self.date_helper.get_days()
        }

        menu(mock_msg)

        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('menu_response.j2', context, error)
        )

    @patch('slackbot.dispatcher.Message', return_value=menu_msg)
    @patch('common.utils.TimetableAPIUtils.make_api_request_for_timetables')
    @patch('plugins.menu_plugin.MenuHelper.get_event', return_value=[])
    @patch('plugins.menu_plugin.MenuHelper.get_meals')
    def test_menu_with_empty_db(self, meals_mock, event_mock, utils_mock, mock_msg):
        mock_msg.body = self.menu
        utils_mock.return_value = []
        context = {
            'timetable_names': [],
            'day_of_week': 'today',
            'no_timetable': True
        }
        menu(mock_msg)

        self.assertTrue(mock_msg.reply.called)
        mock_msg.reply.assert_called_with(
            render('menu_response.j2', context)
        )
