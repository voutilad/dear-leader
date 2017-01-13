import json
import os
from dear_leader.alexa import _is_linked


def test_link_helper():
    """
    Test the logic for checking if the account is linked
    """
    good_session = json.load(
        open(os.path.join(os.path.dirname(__file__), 'fixtures/launch-intent.json'), 'r')
    )
    bad_session = json.load(
        open(os.path.join(os.path.dirname(__file__), 'fixtures/launch-without-link-intent.json'), 'r')
    )

    assert _is_linked(good_session['session']) is True
    assert _is_linked(bad_session['session']) is False
