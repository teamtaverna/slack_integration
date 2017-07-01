import dotenv

from common.utils import render

dotenv.load()

API_TOKEN = dotenv.get('SLACKBOT_API_TOKEN')

DEFAULT_REPLY = render('help_response.j2')

# TO DO:
# The value for ERRORS_TO should be specified in the env file later on
ERRORS_TO = 'bot_test'

PLUGINS = [
    'plugins'
]
