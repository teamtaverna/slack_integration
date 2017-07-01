import re
from operator import itemgetter

from slackbot.bot import respond_to

from common.utils import (get_days, render, make_api_request, date_to_str,
                          list_timetable_names,)


def make_api_request_for_servings(timetable, date):
    query = 'query{servings(timetable:"%s",date:"%s"){publicId, dateServed, vendor{name},\
             menuItem{cycleDay,meal{name},course{name,sequenceOrder},\
             dish{name},timetable{name}}}}' % (timetable, date)
    return make_api_request(query)['servings']


def servings_to_dict(servings):
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


@respond_to('menu', re.IGNORECASE)
def menu(message):
    days = get_days()
    # Convert message text to list to remove multiple spaces that may have
    # been mistakenly added by the user and convert the list back to string
    message_text_list = message.body['text'].lower().split()
    len_msg_text_list = len(message_text_list)
    message_text = ' '.join(message_text_list)
    timetable_names = list_timetable_names()

    if message_text == 'menu':
        num_timetables = len(timetable_names)
        servings = make_api_request_for_servings(
            timetable_names[0], date_to_str('today')
        )

        context = {
            'num_of_timetables': num_timetables,
            'timetable_names': timetable_names
        }

        if num_timetables == 1 and servings is not None:
            meals = servings_to_dict(servings)
            context.update({'meals': meals})

        response = render('menu_response.j2', context)
        message.reply(response)
    elif len_msg_text_list == 2 and message_text_list[1] in timetable_names:
        response = 'Here is the menu for today'
        message.reply(response)
    elif message_text == 'menu today':
        response = 'This is today'
        message.reply(response)
    elif message_text == 'menu tomorrow':
        response = 'This is tomorrow'
        message.reply(response)
    elif len_msg_text_list == 2 and message_text_list[1] in days:
        response = 'This is a weekday'
        message.reply(response)
    else:
        error_msg = 'Wrong menu command'
        response = render('help_response.j2', error=error_msg)
        message.reply(response)
