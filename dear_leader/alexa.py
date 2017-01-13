from __future__ import print_function
import logging
from flask import Blueprint, render_template
from flask_ask import Ask, question, statement, session as ask_session

from dear_leader.settings import accounts
from dear_leader.social_media import get_random_tweet


ask_api = Blueprint('ask_api', __name__)
logger = logging.getLogger(ask_api.name)
ask = Ask(blueprint=ask_api)


@ask.launch
def welcome():
    return question(render_template("welcome"))\
        .reprompt(render_template('pick_a_leader', leaders=accounts.keys()))


@ask.intent('GetNewTweet')
def get_new_tweet():
    return statement('Our Dear Leader said: "' + get_random_tweet(ask_session) + '"')
