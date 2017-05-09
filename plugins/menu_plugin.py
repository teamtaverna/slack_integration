import re

from slackbot.bot import respond_to

from common.utils import get_days, render, make_api_request


def make_api_request_for_timetables():
    query = 'query{timetables{edges{node{name, slug, cycleLength,refCycleDay, \
             vendors{edges{node{name}}}, admins{edges{node{username}}}}}}}'
    return make_api_request(query)['timetables']


def check_num_timetables():
    timetables = make_api_request_for_timetables()
    return len(timetables)


def list_timetable_names():
    timetables = make_api_request_for_timetables()
    return [timetable['slug'] for timetable in timetables]


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
        context = {
            'num_of_timetables': check_num_timetables(),
            'timetable_names': timetable_names
        }
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
