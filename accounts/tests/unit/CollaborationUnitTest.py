from django.contrib.auth.models import User
from rest_framework.test import APIClient, APIRequestFactory, APITestCase, force_authenticate

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

        Test steps:
        - send a request to create a new meal with collaborators
        - check that the meal owner has new pending collaboration objects for those collaborator/meal combos on its
            pending_collaborations prop
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

    def test_user_new_shared_meals(self):
        '''
        Given a user, it should be possible to retrieve all of the pending meals other people have shared with the user
        by accessing the new_shared_meals property.

        Test steps:
        - create a new meal
        - send a patch request to add a collaborator to that meal
        - check that a new pending collaboration object for that meal is present on the collaborator's
            new_shared_meals property.
        '''
        client = APIClient()
        data = {k: v for k, v in self.new_meal_data.items() if k != "collaborators"}
        meal = Meal(**data)
        meal.save()
        meal_id = meal.pk
        meal_owner = meal.owner.username
        user = User.objects.get(username=meal_owner)
        client.force_authenticate(user=user)
        url = "/meals/%d/" % meal_id
        client.patch(url, {"collaborators": [1]}, format="json")
        collaborator = User.objects.get(id=1)
        new_collaboration_exists = collaborator.new_shared_meals.filter(meal=meal).exists()

        self.assertTrue(new_collaboration_exists)
