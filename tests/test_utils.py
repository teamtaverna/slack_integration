import datetime
from unittest import TestCase
from unittest.mock import patch

from freezegun import freeze_time

from common.utils import DateHelper, TimetableAPIUtils


class GetDateTest(TestCase):

    def setUp(self):
        self.helper = DateHelper()

    @freeze_time("2017-03-15")
    def test_yesterday(self):
        yesterday = self.helper.get_date('yesterday')

        self.assertEqual(yesterday, datetime.date(2017, 3, 14))

    @freeze_time("2017-03-15")
    def test_today(self):
        today = self.helper.get_date('today')

        self.assertEqual(today, datetime.date(2017, 3, 15))

    @freeze_time("2017-03-15")
    def test_tomorrow(self):
        tomorrow = self.helper.get_date('tomorrow')

        self.assertEqual(tomorrow, datetime.date(2017, 3, 16))

    def test_misspelt_day(self):
        mistake = 'tooday'

        self.assertRaises(ValueError, self.helper.get_date, mistake)

    @freeze_time("2017-03-15")
    def test_case_insensitivity(self):
        today = self.helper.get_date('TOdaY')

        self.assertEqual(today, datetime.date(2017, 3, 15))

    @freeze_time("2017-03-15")
    def test_get_date_removes_leading_and_trailing_spaces(self):
        day = self.helper.get_date('  today  ')

        self.assertEqual(day, datetime.date(2017, 3, 15))

    @freeze_time("2017-03-15")
    def test_day_of_the_week(self):
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                'saturday', 'sunday', 'today', 'tomorrow', 'yesterday']

        self.assertEqual(self.helper.get_date(days[0]),
                         datetime.date(2017, 3, 13))
        self.assertEqual(self.helper.get_date(days[1]),
                         datetime.date(2017, 3, 14))
        self.assertEqual(self.helper.get_date(days[2]),
                         datetime.date(2017, 3, 15))
        self.assertEqual(self.helper.get_date(days[3]),
                         datetime.date(2017, 3, 16))
        self.assertEqual(self.helper.get_date(days[4]),
                         datetime.date(2017, 3, 17))
        self.assertEqual(self.helper.get_date(days[5]),
                         datetime.date(2017, 3, 18))
        self.assertEqual(self.helper.get_date(days[6]),
                         datetime.date(2017, 3, 19))
        self.assertEqual(self.helper.get_date(days[7]),
                         datetime.date(2017, 3, 15))
        self.assertEqual(self.helper.get_date(days[8]),
                         datetime.date(2017, 3, 16))
        self.assertEqual(self.helper.get_date(days[9]),
                         datetime.date(2017, 3, 14))


class TestAPICalls(TestCase):

    def setUp(self):
        self.timetable_api = TimetableAPIUtils()

    @patch('common.utils.make_api_request')
    def test_make_api_request_for_timetables_with_invalid_token(self, api_mock):
        api_mock.return_value = {'message': 'Invalid Token'}
        timetable_res = self.timetable_api.make_api_request_for_timetables()

        self.assertEqual(timetable_res, [])

    @patch('common.utils.make_api_request')
    def test_make_api_request_for_timetables_with_empty_db(self, api_mock):
        api_mock.return_value = {'timetables': {'edges': []}}
        timetable_res = self.timetable_api.make_api_request_for_timetables()

        self.assertEqual(timetable_res, [])

    @patch('common.utils.make_api_request')
    def test_make_api_request_for_timetables(self, api_mock):
        timetables = [
            {
                'name': 'timetable1',
                'slug': 'timetable1',
                'cycleLength': 5,
                'refCycleDay': 2,
                'vendors': {'edges': []},
                'admins': {'edges': []}
            }
        ]
        api_mock.return_value = {'timetables': timetables}
        timetable_res = self.timetable_api.make_api_request_for_timetables()

        self.assertEqual(timetable_res, timetables)
