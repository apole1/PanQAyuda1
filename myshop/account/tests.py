from django.contrib.auth.models import User
from django.test import TestCase

class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'paulo',
            'password': 'prueba123'}
        User.objects.create_user(**self.credentials)

        self.credentials2 = {
            'username': 'paulo',
            'password': 'prueba1236'}

    def test_login(self):
        # send login data
        response = self.client.post('/account/login/', self.credentials2, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)

    def test_login2(self):
        # send login data
        response = self.client.post('/account/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)

