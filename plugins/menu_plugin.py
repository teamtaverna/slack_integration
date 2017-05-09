import re
import requests

import dotenv
from slackbot.bot import respond_to

from common.utils import get_days


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

    if message.body['text'] == 'menu':
        # TODO: if timetables == 1, return menu for the day
        # else
        # let user know the list of timetables available
        # and the command to use to check

        response = 'This is menu'
        message.reply(response)
    elif message.body['text'].lower() == 'menu today':
        response = 'This is today'
        message.reply(response)
    elif message.body['text'].lower() == 'menu tomorrow':
        response = 'This is tomorrow'
        message.reply(response)
    else:
        if message.body['text'].lower().split()[1] in days:
            response = 'This is a weekday'
            message.reply(response)
