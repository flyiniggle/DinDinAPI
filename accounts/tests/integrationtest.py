from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.authtoken.models import Token

from accounts.views import UserCreate


class AccountsTest(APITestCase):
    test_data = {
        'username': 'Ontario',
        'email': 'foobar@example.com',
        'password': 'somepassword'
    }

    def test_create_user_returns_201(self):
        view = UserCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post("/users/create", self.test_data, format='json')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_works(self):
        view = UserCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post("/users/create", self.test_data, format='json')
        view(request)
        new_user = User.objects.filter(username='Ontario')
        self.assertEqual(new_user.count(), 1)

    def test_create_user_returns_username_and_email(self):
        view = UserCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post("/users/create", self.test_data, format='json')
        response = view(request)
        self.assertEqual(response.data['username'], self.test_data['username'])
        self.assertEqual(response.data['email'], self.test_data['email'])

    def test_create_user_does_not_return_password(self):
        view = UserCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post("/users/create", self.test_data, format='json')
        response = view(request)
        self.assertFalse('password' in response.data)

    def test_create_user_creates_auth_token_for_new_user(self):
        view = UserCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post("/users/create", self.test_data, format='json')
        view(request)
        new_user = User.objects.get(username='Ontario')

        try:
            Token.objects.get(user_id=new_user.id)
        except ObjectDoesNotExist:
            self.fail("No token was created on user creation.")

