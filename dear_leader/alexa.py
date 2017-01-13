from __future__ import print_function
import logging
from flask import Blueprint, render_template
from flask_ask import Ask, question, statement, session as ask_session

from dear_leader.settings import *
from dear_leader.social_media import get_random_tweet


ask_api = Blueprint('ask_api', __name__)
logger = logging.getLogger(ask_api.name)
ask = Ask(blueprint=ask_api)


def _is_linked(session):
    """
    Test if the user has linked their account by checking for an 'accessToken'
    :param session: Ask session
    :return: True if linked, False if not linked.
    """
    if session and 'user' in session:
        return 'accessToken' in session['user']
    return False


@ask.launch
def welcome():
    if _is_linked(ask_session):
        return question(render_template("welcome"))\
            .reprompt(render_template('pick_a_leader', leaders=accounts.keys()))
    return statement(render_template('not_linked'))


@ask.intent('GetNewTweet')
def get_new_tweet():
    leader = ask_session.attributes.get(LEADER_KEY)
    if leader is None:
        return question('You have not declared your Dear Leader!')
    else:
        tweet = get_random_tweet(ask_session)
        return question(render_template('read_tweet', leader=leader, tweet=tweet))


@ask.intent('SelectDearLeader')
def set_leader(leader):
    ask_session.attributes[LEADER_KEY] = leader
    if leader in accounts:
        return question(render_template('leader_set', leader=leader))


@ask.session_ended
def bye():
    return statement(render_template('bye'))
