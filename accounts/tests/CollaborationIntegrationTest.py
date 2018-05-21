from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status

from accounts.views import UserProfile
from meals.views import MealList
from accounts.models import PendingCollaboration


class Collaboration(APITestCase):
    fixtures = ['mealsdump.json', 'authdump.json',]
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
        response = view(request)

        pending_collaborations = PendingCollaboration.objects.all()
        self.assertEqual(len(pending_collaborations), 2)

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
    