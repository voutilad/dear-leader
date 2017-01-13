"""
Integration to Twitter and other Social Media Sources
"""
from __future__ import print_function
import os
import random
import twitter


TWITTER_CONSUMER_KEY=os.environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET=os.environ['TWITTER_CONSUMER_SECRET']


def get_random_tweet(session, screen_name='realDonaldTrump'):
    """
    Grab token from session and get a tweet!
    """
    token = session['user']['accessToken'].split(',')
    key, secret = token[0], token[1]
    api = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
                      consumer_secret=TWITTER_CONSUMER_SECRET,
                      access_token_key=key, access_token_secret=secret)

    timeline = api.GetUserTimeline(screen_name=screen_name,
                                   include_rts=False,
                                   trim_user=True,
                                   exclude_replies=True,
                                   count=100)

    index = random.randint(0, len(timeline)-1)
    tweet = timeline[index]
    return tweet.text