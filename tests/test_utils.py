import datetime
import unittest

from freezegun import freeze_time

from common.utils import TimeService


class TimeServiceTest(unittest.TestCase):

    @freeze_time("2017-03-15")
    def test_yesterday(self):
        yesterday = TimeService.yesterday(self)

        self.assertEqual(yesterday, datetime.date(2017, 3, 14))

    @freeze_time("2017-03-15")
    def test_today(self):
        today = TimeService.today(self)

        self.assertEqual(today, datetime.date(2017, 3, 15))

    @freeze_time("2017-03-15")
    def test_tomorrow(self):
        tomorrow = TimeService.tomorrow(self)

        self.assertEqual(tomorrow, datetime.date(2017, 3, 16))
