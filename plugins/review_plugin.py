import re
import hashlib

from slackbot.bot import respond_to

from common.utils import render, make_api_request


class ReviewHelper:

    @staticmethod
    def make_api_request_for_review(serving_id, rating_value, anonymity_id, comment=''):
        query = 'mutation{createReview(input: {serving: "%s", value: "%s", \
                anonymityId: "%s", comment: "%s"})\
                {review{id,originalId,value,comment,anonymityId,serving{publicId}}}}' % \
                (serving_id, rating_value, anonymity_id, comment)
        res = make_api_request(query)

        if 'review' in res:
            if res['review'] is None:
                return 'duplicate'
            else:
                return 'success'

    @staticmethod
    def hash_string(string):
        string = string.encode()
        return hashlib.sha224(string).hexdigest()

    @staticmethod
    def render_template_with_error(message, error):
        response = render('review_response.j2', error=error)
        message.reply(response)

    @staticmethod
    def render_template_with_context(message, context):
        response = render('review_response.j2', context=context)
        message.reply(response)


@respond_to('rate', re.IGNORECASE)
def review(message):
    message_text_list = message.body['text'].lower().split()

    if len(message_text_list) < 3:
        error = 'You entered a wrong rating format.'
        ReviewHelper.render_template_with_error(message, error)
    else:
        serving_id = message_text_list[1]
        rating_value = int(message_text_list[2])

        # Check that rating value is of valid range (1 - 5)
        if rating_value not in range(1, 6):
            error = 'Invalid rating value.'
            ReviewHelper.render_template_with_error(message, error)
            return

        anonymity_id = ReviewHelper.hash_string(message.body['user'])
        if len(message_text_list) > 3:
            comment = message_text_list[3:]
            review = ReviewHelper.make_api_request_for_review(
                serving_id, rating_value, anonymity_id, comment
            )
        else:
            review = ReviewHelper.make_api_request_for_review(
                serving_id, rating_value, anonymity_id
            )

        if review == 'duplicate':
            context = {
                'duplicate': True
            }
            ReviewHelper.render_template_with_context(message, context)
        elif review == 'success':
            context = {
                'success': True
            }
            ReviewHelper.render_template_with_context(message, context)
        else:
            error = 'Invalid menu id.'
            ReviewHelper.render_template_with_error(message, error)
