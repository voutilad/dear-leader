"""
Test the interaction and statefulness
"""
import os
from unittest.mock import patch
from dear_leader.server import create_app
from dear_leader.settings import CLIENT_ID


app = create_app()
app.config['TESTING'] = True
client = app.test_client()


def test_if_get_to_index_redirects_to_github():
    """
    Make sure we send requests to our home/index page to Github.
    """
    response = client.get('/', follow_redirects=False)
    assert response is not None
    assert response.status_code == 302
    assert response.location == 'https://github.com/voutilad/dear-leader'


def test_bad_client_id_results_in_403():
    """
    If we don't get the correct client-id, forbid going any further.
    """
    response = client.get('/oauth/authorize?client_id=abc&state=123')
    assert response is not None
    assert response.status_code == 403


def test_redirect_to_twitter_oauth():
    """
    Given valid client-id and a state, we should redirect to twitter
    """
    response = client.get('/oauth/authorize?client_id=' + CLIENT_ID +
                          '&state=123')
    assert response is not None
    assert response.status_code == 302
    assert 'https://api.twitter.com/oauth/authorize' in response.location


def test_json_response_from_alexa():
    data = open(os.path.join(os.path.dirname(__file__), 'fixtures/launch-intent.json'), 'r').read()
    response = client.post('/ask', data=data)

    assert response is not None
    assert response.status_code == 200
    assert b'Our Dear Leader welcomes you!' in response.data
    assert b'You can say any of the following' in response.data
    assert b'President' in response.data


@patch('dear_leader.alexa.get_random_tweet', return_value="hey now!")
def test_getting_new_tweet(mock):
    data = open(os.path.join(os.path.dirname(__file__), 'fixtures/GetNewTweet-intent.json'), 'r').read()
    response = client.post('/ask', data=data)

    assert response is not None
    assert response.status_code == 200
    assert b'Our Dear Leader said: \\"hey now!\\"' in response.data
