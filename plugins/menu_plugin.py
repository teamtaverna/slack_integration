import re
from operator import itemgetter

from dateutil import parser
from slackbot.bot import respond_to

from common.utils import (get_days, render, make_api_request, date_to_str,
                          list_timetable_names,)


class MenuHelper:
    """Contains helper functions for menu response."""

    def make_api_request_for_servings(self, timetable, date):
        query = 'query{servings(timetable:"%s",date:"%s"){publicId, dateServed, vendor{name},\
                 menuItem{cycleDay,meal{name},course{name,sequenceOrder},\
                 dish{name},timetable{name}}}}' % (timetable, date)
        return make_api_request(query)['servings']

    def make_api_request_for_events(self):
        query = 'query {events{edges{node{name, action, startDate, endDate}}}}'
        events = make_api_request(query)['events']
        if 'edges' not in events:
            return events

    def servings_to_dict(self, servings):
        new_dict = {}

        for obj in servings:
            meal = obj['menuItem']['meal']['name']
            menu_item = obj['menuItem']
            new_obj = {
                'public_id': obj['publicId'],
                'course': menu_item['course']['name'],
                'sequence_order': menu_item['course']['sequenceOrder'],
                'dish': menu_item['dish']['name']
            }
            if new_dict.get(meal):
                new_dict[meal].append(new_obj)
            else:
                new_dict[meal] = [new_obj]

        # Re-order the meals by sequence order
        return {
            key: sorted(
                value,
                key=itemgetter('sequence_order')
            ) for key, value in new_dict.items()
        }

    def get_meals(self, timetable, day):
        """
        Get meals for a particular timetable.
        day is a string either today, tomorrow, yesterday, or any weekday
        """
        servings = self.make_api_request_for_servings(
            timetable, date_to_str(day)
        )

        if servings is not None:
            meals = self.servings_to_dict(servings)
            return meals

    def get_event(self, day):
        events = self.make_api_request_for_events()
        event_list = []

        if events:
            date = parser.parse(date_to_str(day)).isoformat()
            for event in events:
                start_date = parser.parse(event['startDate']).isoformat()
                end_date = parser.parse(event['endDate']).isoformat()

                if (date >= start_date) and (date <= end_date):
                    event_list.append(event)
        return event_list

    def meals_check_context_update(self, meals, context, day):
        if meals and not self.get_event(day):
            context.update({'meals': meals})
        else:
            context.update({'no_meals': True})


@respond_to('menu', re.IGNORECASE)
def menu(message):
    helper = MenuHelper()
    days = get_days()
    # Convert message text to list to remove multiple spaces that may have
    # been mistakenly added by the user and convert the list back to string
    message_text_list = message.body['text'].lower().split()
    len_msg_text_list = len(message_text_list)
    message_text = ' '.join(message_text_list)
    timetable_names = list_timetable_names()

    if len_msg_text_list > 1:
        timetable_name = message_text_list[1]

    if len_msg_text_list > 2:
        day_of_week = message_text_list[2]

    num_timetables = len(timetable_names)

    context = {
        'timetable_names': timetable_names,
        'day_of_week': 'today'
    }

    if message_text == 'menu':
        if num_timetables == 1:
            meals = helper.get_meals(timetable_names[0], 'today')
            helper.meals_check_context_update(meals, context, 'today')
        else:
            context.update({'multiple_timetables': True})

        response = render('menu_response.j2', context)
        message.reply(response)

    elif len_msg_text_list == 2 and timetable_name in timetable_names:
        # User entered "menu TIMETABLE_NAME"
        meals = helper.get_meals(timetable_name, 'today')
        helper.meals_check_context_update(meals, context, 'today')

        response = render('menu_response.j2', context)
        message.reply(response)

    elif (len_msg_text_list == 3 and
          timetable_name in timetable_names and
          day_of_week in days):
        # User entered "menu TIMETABLE_NAME day"
        meals = helper.get_meals(timetable_name, day_of_week)
        context.update({'day_of_week': day_of_week})
        helper.meals_check_context_update(meals, context, day_of_week)

        response = render('menu_response.j2', context)
        message.reply(response)

    else:
        response = render('help_response.j2')
        message.reply(response)
