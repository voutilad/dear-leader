"""
Tests for interacting with Twitter
"""
import os
from dear_leader import social_media


ACCESS_TOKEN_KEY = os.environ['TWITTER_ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_SECRET']

ACCESS_TOKEN = ACCESS_TOKEN_KEY + "," + ACCESS_TOKEN_SECRET
FAKE_SESSION = {"user": {"accessToken": ACCESS_TOKEN}}


def test_if_we_can_get_a_tweet():
    """
    Test if we can hit Twitter's timeline api and grab a tweet.
    """
    text = social_media.get_random_tweet(FAKE_SESSION)
    assert text is not None
    assert len(text) > 0
