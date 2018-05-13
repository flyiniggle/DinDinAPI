from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token

from accounts.views import UserCreate, UserList


class CreateUserTest(APITestCase):
    fixtures = ['authdump.json']
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
        self.assertNotIn('password', response.data)

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

    def test_create_user_fails_with_no_user_name(self):
        view = UserCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post("/users/create", {"email": "me@home.com", "password": "superstrong!"}, format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_create_user_fails_with_duplicate_user_name(self):
        view = UserCreate.as_view()
        factory = APIRequestFactory()
        existing_user = User.objects.first()
        request = factory.post("/users/create",
                               {"username": existing_user.username, "email": "me@home.com", "password": "superstrong!"},
                               format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_create_user_fails_with_no_email(self):
        view = UserCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post("/users/create", {"username": "Shaq", "password": "superstrong!"}, format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_create_user_fails_with_invalid_email(self):
        view = UserCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post("/users/create",
                               {"username": "Shaq", "email": "meh", "password": "superstrong!"},
                               format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_create_user_fails_with_no_password(self):
        view = UserCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post("/users/create", {"username": "Shaq", "email": "me@home.com"}, format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_create_user_fails_with_short_password(self):
        view = UserCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post("/users/create",
                               {"username": "Shaq", "email": "me@home.com", "password": "hey"},
                               format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_create_user_fails_with_similar_password_and_username(self):
        view = UserCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post("/users/create",
                               {"username": "iamawesome", "email": "me@home.com", "password": "iamawesome"},
                               format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_create_user_fails_with_common_passwords(self):
        view = UserCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post("/users/create",
                               {"username": "Shaq", "email": "me@home.com", "password": "password"},
                               format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_create_user_fails_with_numeric_passwords(self):
        view = UserCreate.as_view()
        factory = APIRequestFactory()
        request = factory.post("/users/create",
                               {"username": "Shaq", "email": "me@home.com", "password": "11111111111111"},
                               format='json')
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)


class UserListTest(APITestCase):
    fixtures = ['authdump.json']

    def test_get_users_should_return_200(self):
        view = UserList.as_view()
        factory = APIRequestFactory()
        request = factory.get('users', format='json')
        user = User.objects.get(username='test')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users_should_return_all_users(self):
        view = UserList.as_view()
        factory = APIRequestFactory()
        request = factory.get('users', format='json')
        user = User.objects.get(username='test')
        force_authenticate(request, user=user)
        response = view(request)

        users = User.objects.all()

        for user in response.data:
            with self.subTest(user=user):
                self.assertEqual(users.filter(username=user.get("username")).count(), 1)