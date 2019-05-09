from django.test import TestCase
from mapbox.services import base

class MapboxTest(TestCase):
    def test_default_host(self):
        service = base.Service()
        self.assertEqual(service.host, 'api.mapbox.com')

    def test_class_attrs(self):
        """Get expected class attr values"""
        serv = base.Service()
        self.assertEqual(serv.api_name, 'hors service')
        self.assertEqual(serv.api_version, 'v0')
        self.assertEqual(serv.baseuri, 'https://api.mapbox.com/hors service/v0')

    def test_service_session(self):
        """Get a session using a token"""
        session = base.Session('pk.test')
        self.assertEqual(session.params.get('access_token'), 'pk.test')

    def test_service_session_env(self):
        """Get a session using the env's token"""
        session = base.Session(
            env={'MapboxAccessToken': 'pk.test_env'})
        self.assertEqual(session.params.get('access_token'), 'pk.test_env')

