from __future__ import print_function
import os
from flask import Flask, url_for, request, redirect, session
from flask_oauthlib.client import OAuth
from flask_oauthlib.contrib.apps import twitter

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']
oauth = OAuth(app)
twitter = oauth.remote_app(
    'twitter',
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize'
)

@app.route('/authorize')
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

    print('DEBUG [state=' + str(state) + ']')
    print('DEBUG [client_id=' + str(client_id) + ']')
    print('DEBUG [redirect_uri=' + str(redirect_uri) + ']')

    if state and client_id:
        session['state'] = state

        if client_id == 'alexa-trump':
            callback_url = url_for('oauth_callback', next=redirect_uri)
            return twitter.authorize(callback=callback_url)
        else:
            return 'bad client_id: ' + client_id

    return '<html><body>Hey, man. Are you using Alexa or not?</body></html>'


@app.route('/callback')
def oauth_callback():
    resp = twitter.authorized_response()
    token = str(resp['oauth_token']) + ',' + str(resp['oauth_token_secret'])
    token_type = 'Bearer'
    print('DEBUG [resp=' + str(resp) + ']')

    if resp:
        next_url = request.args.get('next') + '&state=' + session['state'] + \
            '&access_token=' + str(token) + '&token_type=' + str(token_type)
        print('DEBUG [next_url=' + str(next_url) + ']')
        return redirect(next_url)
    else:
        return 'Failed to authorize :-('

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
