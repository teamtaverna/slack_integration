import re

from slackbot.bot import respond_to

from common.utils import render, list_timetable_names


@respond_to('timetable', re.IGNORECASE)
def timetable(message):
    timetable_names = list_timetable_names()
    context = {
        'timetable_names': timetable_names
    }
    response = render('timetable_response.j2', context)
    message.reply(response)
