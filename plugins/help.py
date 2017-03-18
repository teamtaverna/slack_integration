import os
import re

import jinja2
from slackbot.bot import respond_to


def render(template_path, context=None):
    path, filename = os.path.split(template_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)


@respond_to('help', re.IGNORECASE)
def help(message):
    response = render('../templates/help_response.j2')
    message.reply(response)
