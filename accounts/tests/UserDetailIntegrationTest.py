from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from accounts.views import UserDetail


class UserDetailTest(APITestCase):
    fixtures = ['authdump.json']

    def test_get_user_detail_should_return_200(self):
        view = UserDetail.as_view()
        factory = APIRequestFactory()
        request = factory.get('users', format='json')
        user = User.objects.get(username='test')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail_should_return_401_if_unauthorized(self):
        view = UserDetail.as_view()
        factory = APIRequestFactory()
        request = factory.get('users', format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_detail_should_return_profile_of_logged_in_user(self):
        view = UserDetail.as_view()
        factory = APIRequestFactory()
        request = factory.get('users', format='json')
        user = User.objects.get(username='test')
        force_authenticate(request, user=user)
        response = view(request)
        data = response.data

        self.assertIn("id", data)
        self.assertIn("email", data)
        self.assertIn("username", data)
        self.assertEqual(data.get("username"), "test")