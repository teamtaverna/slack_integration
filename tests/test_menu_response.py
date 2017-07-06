from unittest import TestCase
from unittest.mock import patch

from plugins.menu_plugin import MenuHelper, menu
from faker import fake_creds, FakeClient, FakeMessage
from common.utils import render


class MenuHelperTest(TestCase):
    servings = [
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

    def setUp(self):
        self.menu_helper = MenuHelper()
        self.sorted_servings = {
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

    @patch('common.utils.date_to_str', return_value='2017-07-06')
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

    @patch('common.utils.date_to_str', return_value='2017-07-06')
    @patch('plugins.menu_plugin.MenuHelper.make_api_request_for_events')
    def test_present_events(self, mock_event, day_mock):
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

    @patch('common.utils.date_to_str', return_value='2017-07-06')
    @patch('plugins.menu_plugin.MenuHelper.make_api_request_for_events')
    def test_no_event(self, mock_event, day_mock):
        mock_event.return_value = []
        events = self.menu_helper.get_event('today')

        self.assertEqual(events, [])

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
