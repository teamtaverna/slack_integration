import re
import requests

import dotenv
from slackbot.bot import respond_to

from common.utils import get_days, render

dotenv.load()


def make_api_request_for_timetables():
    api_url = dotenv.get('API_URL_ENDPOINT')
    query = 'query{timetables{edges{node{name, cycleLength,refCycleDay, \
             vendors{edges{node{name}}}, admins{edges{node{username}}}}}}}'
    endpoint = '{}?query={}'.format(api_url, query)
    headers = {'X-TavernaToken': dotenv.get('X-TAVERNATOKEN')}
    return requests.post(endpoint, headers=headers).json()['timetables']


def check_num_available_timetables():
    timetables = make_api_request_for_timetables()
    return len(timetables)


@respond_to('menu', re.IGNORECASE)
def menu(message):
    days = get_days()
    num_of_timetables = check_num_available_timetables()
    # Convert message text to list to remove multiple spaces that may have
    # been mistakenly added by the user and convert the list back to string
    message_text_list = message.body['text'].lower().split()
    message_text = ' '.join(message_text_list)

    if message_text == 'menu':
        context = {
            'num_of_timetables': num_of_timetables
        }
        response = render('menu_response.j2', context)
        message.reply(response)
    elif message_text == 'menu today':
        response = 'This is today'
        message.reply(response)
    elif message_text == 'menu tomorrow':
        response = 'This is tomorrow'
        message.reply(response)
    # Add one more check for if the user enters `menu timetable_name`
    else:
        if message_text_list[1] in days:
            response = 'This is a weekday'
            message.reply(response)
        else:
            response = 'Wrong command yo! Type help to get help.'
            message.reply(response)
