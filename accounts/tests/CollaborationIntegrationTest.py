from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from accounts.models import PendingCollaboration
from accounts.views import UserCollaborations
from meals.views import MealList


class Collaboration(APITestCase):
    fixtures = ['dump.json']
    new_meal_data = {
        "name": "turkey goop",
        "taste": 3,
        "difficulty": 2,
        "last_used": "2018-03-13",
        "used_count": 4,
        "notes": "classic",
        "collaborators": [2, 3]
    }

    def test_add_pending_collaborator_on_meal_creation(self):
        view = MealList.as_view()
        factory = APIRequestFactory()
        request = factory.post('meals', self.new_meal_data, format='json')
        user = User.objects.get(username='admin')
        force_authenticate(request, user=user)
        view(request)

        self.assertEqual(len(user.new_shared_meals.all()), 3)

    def test_get_pending_collaborations_returns_200(self):
        view = UserCollaborations.as_view()
        factory = APIRequestFactory()
        request = factory.get("user/pending")
        user = User.objects.get(username='admin')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_pending_collaborations_returns_401_if_user_is_unauthenticated(self):
        view = UserCollaborations.as_view()
        factory = APIRequestFactory()
        request = factory.get("user/pending")
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_pending_collaborations_returns_list_of_pending_shared_meals_for_user(self):
        view = UserCollaborations.as_view()
        factory = APIRequestFactory()
        request = factory.get("user/pending")
        user = User.objects.get(username='admin')
        force_authenticate(request, user=user)
        response = view(request)

        pending_meals = PendingCollaboration.objects.filter(collaborator=user)
        for pending_collaboration in response.data:
            with self.subTest(pending_collaboration=pending_collaboration):
                self.assertIsNotNone(pending_meals.filter(meal=pending_collaboration["meal"]))

    def test_accept_collaboration(self):
        pass

    def test_decline_collaboration(self):
        pass

    def test_add_collaboration_to_existing_meal(self):
        pass

    def test_owner_remove_collaborator_from_existing_meal(self):
        pass

    def test_collaborator_remove_self_from_existing_meal(self):
        pass
