import re

from slackbot.bot import respond_to

from common.utils import render, TimetableAPIUtils


@respond_to('show timetable', re.IGNORECASE)
def timetable(message):
    message_text_list = message.body['text'].lower().split()
    len_msg_text_list = len(message_text_list)

    if len_msg_text_list == 2 and message_text_list[1] == 'timetable':
        timetable_res = TimetableAPIUtils()
        timetable_names = timetable_res.list_timetable_names()
        context = {
            'timetable_names': timetable_names
        }
        response = render('timetable_response.j2', context)
    else:
        response = render('help_response.j2')
    message.reply(response)
