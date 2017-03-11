import dotenv

dotenv.load()

API_TOKEN = dotenv.get('SLACKBOT_API_TOKEN')
DEFAULT_REPLY = "Sorry, I have not been fully configured yet."

# TO DO:
# The value for ERRORS_TO should be specified in the env file later on
ERRORS_TO = 'bot_test'

PLUGINS = [
    'slackbot.plugins',
    'plugins',
]
