from __future__ import print_function
import logging
import os
from flask import Blueprint, url_for, request, redirect, session, abort, current_app
from flask_oauthlib.client import OAuth
from dear_leader.settings import CLIENT_ID

oauth_api = Blueprint('oauth_api', __name__)
logger = logging.getLogger(oauth_api.name)


def get_oauth_client(app):
    if hasattr(app, 'oauth_client'):
        return app.oauth_client
    else:
        client = OAuth(app).remote_app(
            'twitter',
            consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
            consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
            base_url='https://api.twitter.com/1.1/',
            request_token_url='https://api.twitter.com/oauth/request_token',
            access_token_url='https://api.twitter.com/oauth/access_token',
            authorize_url='https://api.twitter.com/oauth/authorize')
        app.oauth_client = client
        return client
    return None


@oauth_api.route('/authorize')
def authorize():
    """
    The Alexa app should call this, passing in 'state', 'client_id',
    'response_type', 'scope', and a 'redirect_uri'. We need 'state' and the
    generated oauth code. We don't use 'scope' at the moment.
    """
    # i think this is unique and generated by Amazon
    state = request.args.get('state')

    # this should match what we set in the Alexa skill config online
    client_id = request.args.get('client_id')

    # Amazon should provide this, but does give us static values in the
    # online Alexa skill config...not sure why
    redirect_uri = request.args.get('redirect_uri')

    logger.debug('state=' + str(state) + '')
    logger.debug('client_id=' + str(client_id))
    logger.debug('redirect_uri=' + str(redirect_uri))

    if state and client_id:
        session['state'] = state

        if client_id == CLIENT_ID:
            callback_url = url_for('oauth_api.oauth_callback', next=redirect_uri)
            return get_oauth_client(current_app).authorize(callback=callback_url)
        else:
            logger.info('bad client_id')
            abort(403)

        logger.info('Did not find both a valid state and client_id.')
    return '<html><body>Hey, man. Are you using Alexa or not?</body></html>'


@oauth_api.route('/callback')
def oauth_callback():
    resp = get_oauth_client(current_app).authorized_response()
    token = str(resp['oauth_token']) + ',' + str(resp['oauth_token_secret'])
    token_type = 'Bearer'

    if resp:
        # JFC...we need a HASH before our attributes! THANKS AMAZON.
        next_url = request.args.get('next') + '#state=' + session['state'] + \
            '&access_token=' + str(token) + '&token_type=' + str(token_type)
        logger.debug('next_url=' + str(next_url))
        return redirect(next_url)
    else:
        logger.info('Failed to authorize')
        return 'Failed to authorize :-('
