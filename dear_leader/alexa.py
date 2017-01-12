from __future__ import print_function
import logging
from flask import Blueprint, render_template, session
from flask_ask import Ask, question, statement
from dear_leader import leaders


ask_api = Blueprint('ask_api', __name__)
logger = logging.getLogger(ask_api.name)
ask = Ask(blueprint=ask_api)


@ask.launch
def welcome():
    return question(render_template("welcome"))\
        .reprompt(render_template('pick_a_leader', leaders=leaders.accounts.keys()))
