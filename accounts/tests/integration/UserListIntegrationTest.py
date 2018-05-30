from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from accounts.views import UserList


class UserListTest(APITestCase):
    fixtures = ['dump.json']

    def test_get_users_should_return_200(self):
        view = UserList.as_view()
        factory = APIRequestFactory()
        request = factory.get('users', format='json')
        user = User.objects.get(username='test3')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users_should_return_401_if_unauthenticated(self):
        view = UserList.as_view()
        factory = APIRequestFactory()
        request = factory.get('users', format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_users_should_return_all_users(self):
        view = UserList.as_view()
        factory = APIRequestFactory()
        request = factory.get('users', format='json')
        user = User.objects.get(username='test3')
        force_authenticate(request, user=user)
        response = view(request)

        users = User.objects.all()

        for user in response.data:
            with self.subTest(user=user):
                self.assertEqual(users.filter(username=user.get("username")).count(), 1)

