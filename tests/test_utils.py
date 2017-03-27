import datetime
import unittest

from freezegun import freeze_time

from common.utils import get_date


class GetDateTest(unittest.TestCase):

    @freeze_time("2017-03-15")
    def test_yesterday(self):
        yesterday = get_date('yesterday')

        self.assertEqual(yesterday, datetime.date(2017, 3, 14))

    @freeze_time("2017-03-15")
    def test_today(self):
        today = get_date('today')

        self.assertEqual(today, datetime.date(2017, 3, 15))

    @freeze_time("2017-03-15")
    def test_tomorrow(self):
        tomorrow = get_date('tomorrow')

        self.assertEqual(tomorrow, datetime.date(2017, 3, 16))

    def test_misspelt_day(self):
        mistake = 'tooday'

        self.assertRaises(ValueError, get_date, mistake)

    @freeze_time("2017-03-15")
    def test_get_date_removes_leading_and_trailing_spaces(self):
        day = get_date('  today  ')

        self.assertEqual(day, datetime.date(2017, 3, 15))

    @freeze_time("2017-03-15")
    def test_day_of_the_week(self):
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                'saturday', 'sunday']

        self.assertEqual(get_date(days[0]), datetime.date(2017, 3, 13))
        self.assertEqual(get_date(days[1]), datetime.date(2017, 3, 14))
        self.assertEqual(get_date(days[2]), datetime.date(2017, 3, 15))
        self.assertEqual(get_date(days[3]), datetime.date(2017, 3, 16))
        self.assertEqual(get_date(days[4]), datetime.date(2017, 3, 17))
        self.assertEqual(get_date(days[5]), datetime.date(2017, 3, 18))
        self.assertEqual(get_date(days[6]), datetime.date(2017, 3, 19))
