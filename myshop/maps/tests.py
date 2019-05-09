from django.test import TestCase
import mapbox
from mapbox.errors import TokenError
from mapbox.services import base

def test_service_session_env():
    """Get a session using the env's token"""
    session = base.Session(
        env={'MapboxAccessToken': 'pk.test_env'})
    assert session.params.get('access_token') == 'pk.test_env'