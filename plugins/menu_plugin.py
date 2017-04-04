import re

from slackbot.bot import respond_to

from common.utils import render, get_date, get_days


def check_available_timetables():
    pass

@respond_to('menu', re.IGNORECASE)
def menu(message):
    days = get_days()

    if message.body['text'] == 'menu':
        timetables = check_available_timetables()
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
