from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate

from meals.models import Meal
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

    def test_user_pending_collaborations(self):
        '''
        Given a user, it should be possible to retrieve all the meals the user has shared with other people
        that are pending acceptance by accessing the pending_collaborations property.
        '''
        view = MealList.as_view()
        factory = APIRequestFactory()
        request = factory.post('meals', self.new_meal_data, format='json')
        user = User.objects.get(username='admin')
        force_authenticate(request, user=user)
        view(request)

        collaborator1 = User.objects.get(pk=2)
        collaborator2 = User.objects.get(pk=3)
        meal = Meal.objects.get(name="turkey goop")

        self.assertIsNotNone(user.pending_collaborations.get(collaborator=collaborator1, meal=meal))
        self.assertIsNotNone(user.pending_collaborations.get(collaborator=collaborator2, meal=meal))
