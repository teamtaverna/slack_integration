import re

from slackbot.bot import respond_to

from common.utils import render


@respond_to('help', re.IGNORECASE)
def help(message):
    response = render('help_response.j2')
    message.reply(response)
