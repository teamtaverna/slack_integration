from datetime import date, timedelta

import jinja2


def get_days():
    return ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday', 'sunday']


def _get_day_arg(day_arg):
    """
    This function takes in a day argument and returns the right timedelta
    days argument for it.
    For example, yesterday will be returned as -1, so that get_date function
    can convert it to the appropriate pythonic date object.
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
        days = get_days()

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


def get_date(day_arg):
    """
    This function handles conversion of date input from users into
    something python can understand. For instance, when the user types
    in something like yesterday, we want to return the date of yesterday.
    """
    day_num = _get_day_arg(day_arg)
    return date.today() + timedelta(days=day_num)


def render(filename, context={}, path='templates'):
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path)
    ).get_template(filename).render(context)
