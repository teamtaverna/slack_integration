import requests
from datetime import date, timedelta

import jinja2
import dotenv

dotenv.load()


class DateHelper:
    """Contains methods for day to date conversion."""

    def get_days(self):
        return ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                'saturday', 'sunday', 'today', 'tomorrow', 'yesterday']

    def _get_day_arg(self, day_arg):
        """
        This method takes in a day argument and returns the right timedelta
        days argument for it.
        For example, yesterday will be returned as -1, so that get_date
        method can convert it to the appropriate pythonic date object.
        We also want to be able to convert weekdays and some date format here.
        """
        day_arg = day_arg.strip().lower()

        day_to_num_dict = {
            'yesterday': -1,
            'today': 0,
            'tomorrow': 1
        }

        day_num = day_to_num_dict.get(day_arg)

        # More logic if a weekday value is passed in.
        if day_num is not None:
            return day_num
        else:
            days = self.get_days()

            if day_arg in days:
                # In python, Monday is 0 and Sunday is 6
                current_weekday_num = date.today().weekday()
                day_index = days.index(day_arg)

                if current_weekday_num == day_index:
                    # The weekday passed in is today
                    return day_to_num_dict['today']
                else:
                    return day_index - current_weekday_num
            else:
                raise ValueError('Cannot resolve date argument passed in.')

    def get_date(self, day_arg):
        """
        This method handles conversion of date input from users into
        something python can understand. For instance, when the user types
        in something like yesterday, we want to return the date of yesterday.
        """
        day_num = self._get_day_arg(day_arg)
        return date.today() + timedelta(days=day_num)

    def date_to_str(self, day_arg):
        """
        This method converts the python date format gotten from
        get_date method to string for graphql api request.
        """
        date = self.get_date(day_arg)
        return date.strftime('%Y-%m-%d')


def render(filename, context={}, error=None, path='templates'):
    if error:
        # Error should be a string
        if isinstance(error, str):
            context['error'] = error
        else:
            raise TypeError('Error message must be a string')
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path)
    ).get_template(filename).render(context)


def make_api_request(query):
    api_url = dotenv.get('API_URL_ENDPOINT')
    endpoint = '{}?query={}'.format(api_url, query)
    headers = {'X-TavernaToken': dotenv.get('X-TAVERNATOKEN')}
    return requests.post(endpoint, headers=headers).json()


class TimetableAPIUtils:
    """Contains shared methods for Timetable API functionality."""

    def make_api_request_for_timetables(self):
        query = 'query{timetables{edges{node{name, slug, cycleLength, refCycleDay, isActive\
                 vendors{edges{node{name}}}, admins{edges{node{username}}}}}}}'
        res = make_api_request(query)
        timetables = res.get('timetables')
        if timetables and 'edges' not in timetables:
            return [timetable for timetable in timetables if timetable['isActive']]
        else:
            return []

    def list_timetable_names(self):
        timetables = self.make_api_request_for_timetables()
        return [timetable['slug'] for timetable in timetables]
