import re

from slackbot.bot import respond_to

from common.utils import render


def make_api_request_for_review(self, public_id, rating_value, anonymity_id, comment=None):
    query = 'mutation{createReview(input: {serving: "%s", value: "%s", comment: "%s"})\
            {review{id,originalId,value,comment,serving{publicId}}}}' % \
            (public_id, rating_value, comment)
    res = make_api_request(query)


@respond_to('rate', re.IGNORECASE)
def review(message):
    message_text_list = message.body['text'].lower().split()
    if len(message_text_list) < 3:
        error = 'You entered a wrong rating format.'
        response = render('review_response.j2', error=error)
        message.reply(response)
    else:
        serving_id = message_text_list[1]
        rating_value = message_text_list[2]
    if len(message_text_list) > 3:
        comment = message_text_list[3:]

    # Check that rating value is of valid range (1 - 5)
    if rating_value not in range(1, 6):
        error = 'Invalid rating value.'
        response = render('review_response.j2', error=error)
        message.reply(response)



# wblav42j
