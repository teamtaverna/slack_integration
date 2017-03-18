from datetime import date, timedelta


class TimeService:
    """
    This class handles conversion of date input from users into
    something python can understand. For instance, when the user types
    in something like yesterday, we want to return the date of yesterday.
    """

    def yesterday(self):
        return date.today() - timedelta(days=1)

    def today(self):
        return date.today()

    def tomorrow(self):
        return date.today() + timedelta(days=1)
