"""
Tests for Alexa Intents using Flask-Ask
"""
from dear_leader import alexa, server, settings
from unittest import mock
import pytest

app = server.create_app()


def text_from_statement(statement):
    return statement._response['outputSpeech']['text']


def reprompt_from_statement(statement):
    return statement._response['reprompt']['outputSpeech']['text']


def card_from_statement(statement):
    return statement._response['card']['text'], \
           statement._response['card']['title']


def has_reprompt(statement):
    return 'reprompt' in statement._response


@pytest.mark.skip
@mock.patch('dear_leader.alexa._is_linked', return_value=True)
def test_welcome_when_linked(mock):
    """
    Are we prompted to setup our skill on first welcome?
    """
    with app.test_request_context():
        statement = alexa.welcome()
        assert "Our Dear Leader welcomes you!" in text_from_statement(statement)
        assert "You can say any of the following" in text_from_statement(statement)

        assert has_reprompt(statement)
        reprompt_text = reprompt_from_statement(statement)
        assert "You can say any of the following" in reprompt_text

        for leader in settings.accounts:
            assert leader in reprompt_text


@pytest.mark.skip
@mock.patch('dear_leader.alexa.get_random_tweet', return_value='hey')
def test_get_new_tweet(mock):
    """
    test getting a new tweet
    """
    with app.test_request_context():
        # no slot filled
        question = alexa.get_new_tweet()
        assert question is not None
        assert 'You have not declared your Dear Leader' in text_from_statement(question)

        # slot filled
        statement = alexa.get_new_tweet()
        assert statement is not None
        assert 'The President of the United States said' in text_from_statement(statement)


