from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory

from meals.models import Meal
from meals.views import MealDetail


class GetMealDetailTest(TestCase):
    fixtures = ['dump.json',]

    def test_get_meal_returns_200_status(self):
        client = APIClient()
        meal = Meal.objects.first()
        meal_id = meal.pk
        meal_owner = meal.owner.username
        user = User.objects.get(username=meal_owner)
        client.force_authenticate(user=user)
        url = "/meals/%d/" % meal_id
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_meal_returns_relevant_fields(self):
        '''
        A request to get a specific meal should return a meal object with the appropriate data in it.

        Test steps:
        - send a request to get a specific meal
        - check that the response data has the appropriate properties
        '''
        client = APIClient()
        meal = Meal.objects.first()
        meal_id = meal.pk
        meal_owner = meal.owner.username
        user = User.objects.get(username=meal_owner)
        client.force_authenticate(user=user)
        url = "/meals/%d/" % meal_id
        response = client.get(url)
        meal = response.data

        self.assertIn("pk", meal)
        self.assertIn("name", meal)
        self.assertIn("owner", meal)
        self.assertIn("collaborators", meal)
        self.assertIn("taste", meal)
        self.assertIn("difficulty", meal)
        self.assertIn("last_used", meal)
        self.assertIn("used_count", meal)
        self.assertIn("notes", meal)
        self.assertIn("ingredients", meal)


class UpdateMealDetailTest(TestCase):
    fixtures = ['dump.json', ]

    def test_update_meal(self):
        '''
        Sending a request to update a specific meal should result in that meal's data being changed.

        Test steps
        - defined edits for a meal
        - make a request to update a meal with the edit data
        - check that the meal db object has been updated with the new data
        '''
        updated_data = {
            "name": "test meal",
            "taste": 1,
            "difficulty": 1,
            "last_used": "2018-01-01",
            "used_count": 22,
            "notes": "test notes",
            "ingredients": ["sugar", "spice", "everything nice"]
        }
        client = APIClient()
        meal = Meal.objects.first()
        meal_id = meal.pk
        meal_owner = meal.owner.username
        user = User.objects.get(username=meal_owner)
        client.force_authenticate(user=user)
        url = "/meals/%d/" % meal_id
        client.patch(url, updated_data, format="json")
        meal.refresh_from_db()

        self.assertEqual(meal.name, updated_data["name"])
        self.assertEqual(meal.taste, updated_data["taste"])
        self.assertEqual(meal.difficulty, updated_data["difficulty"])
        self.assertEqual(meal.last_used.strftime("%Y-%m-%d"), updated_data["last_used"])
        self.assertEqual(meal.used_count, updated_data["used_count"])
        self.assertEqual(meal.notes, updated_data["notes"])
        self.assertEqual(meal.ingredients, updated_data["ingredients"])

    def test_update_meal_returns_200(self):
        updated_data = {
            "name": "test meal",
            "taste": 1,
            "difficulty": 1,
            "notes": "test notes"
        }
        client = APIClient()
        meal = Meal.objects.first()
        meal_id = meal.pk
        meal_owner = meal.owner.username
        user = User.objects.get(username=meal_owner)
        client.force_authenticate(user=user)
        url = "/meals/%d/" % meal_id
        response = client.patch(url, updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_meal_returns_meal_data(self):
        '''
        A successful request to update a meal record should return the update meal data.

        Test steps
        - define updated meal data
        - make a request to update a meal
        - check that the response data reflects the updated meal info
        '''
        updated_data = {
            "name": "test meal",
            "taste": 1,
            "difficulty": 1,
            "last_used": "2018-01-01",
            "used_count": 22,
            "notes": "test notes",
            "ingredients": ["sugar", "spice", "everything nice"]
        }
        client = APIClient()
        meal = Meal.objects.first()
        meal_id = meal.pk
        meal_owner = meal.owner.username
        user = User.objects.get(username=meal_owner)
        client.force_authenticate(user=user)
        url = "/meals/%d/" % meal_id
        response = client.patch(url, updated_data, format="json")
        meal = response.data

        self.assertIn("pk", meal)
        self.assertIn("name", meal)
        self.assertIn("owner", meal)
        self.assertIn("collaborators", meal)
        self.assertIn("taste", meal)
        self.assertIn("difficulty", meal)
        self.assertIn("last_used", meal)
        self.assertIn("used_count", meal)
        self.assertIn("notes", meal)
        self.assertIn("ingredients", meal)

        self.assertEqual(meal["name"], updated_data["name"])
        self.assertEqual(meal["taste"], updated_data["taste"])
        self.assertEqual(meal["difficulty"], updated_data["difficulty"])
        self.assertEqual(meal["last_used"], updated_data["last_used"])
        self.assertEqual(meal["used_count"], updated_data["used_count"])
        self.assertEqual(meal["notes"], updated_data["notes"])
        self.assertEqual(meal["ingredients"], updated_data["ingredients"])

    def test_update_owner_fails(self):
        client = APIClient()
        meal = Meal.objects.first()
        meal_id = meal.pk
        meal_owner = meal.owner
        owner_name = meal_owner.username
        user = User.objects.get(username=owner_name)
        client.force_authenticate(user=user)
        url = "/meals/%d/" % meal_id
        response = client.patch(url, {"owner": 3}, format="json")
        meal.refresh_from_db()

        self.assertEqual(meal.owner, meal_owner)
        self.assertEqual(response.data["owner"], meal_owner.username)

    def test_update_collaborators_fails(self):
        client = APIClient()
        meal = Meal.objects.first()
        meal_id = meal.pk
        collaborators = meal.collaborators
        user = meal.owner
        client.force_authenticate(user=user)
        url = "/meals/%d/" % meal_id
        response = client.patch(url, {"collaborators": [3]}, format="json")
        meal.refresh_from_db()

        self.assertEqual(meal.collaborators, collaborators)
        self.assertEqual(response.data["collaborators"], list(collaborators.all()))

    def test_get_meals_returns_404_status_if_logged_in_as_different_user(self):
        client = APIClient()
        user = User.objects.get(username='test2')
        client.force_authenticate(user=user)
        meal = Meal.objects.filter(owner_id=1).first()
        meal_id = meal.pk
        url = "/meals/%d/" % meal_id
        response = client.get(url, format="json")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.status_text, 'Not Found')

    def test_get_meals_returns_401_status_if_not_logged_in(self):
        factory = APIRequestFactory()
        meal = Meal.objects.first()
        meal_id = meal.pk
        url = "meals//%d/" % meal_id
        request = factory.get(url)
        view = MealDetail.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.status_text, 'Unauthorized')

    def test_update_ingredients_replaces_ingredients_list(self):
        '''
        When a meal's ingredients are updated, the old ingredients list should be entirely replaced by the new one.

        Test steps:
        - create a meal with ingredients
        - send a request to update that meal's ingredients
        - check that the meal db object's incredients list reflects the update list.
        '''
        new_meal_data = {
            "name": "test meal",
            "taste": 1,
            "difficulty": 1,
            "last_used": "2018-01-01",
            "used_count": 22,
            "notes": "test notes",
            "ingredients": ["sugar", "spice", "everything nice"]
        }
        new_meal = Meal(**new_meal_data)
        new_meal.save()
        meal_id = new_meal.pk

        updated_ingredients = {
            "ingredients": ["lemon", "lime"]
        }
        user = new_meal.owner
        client = APIClient()
        client.force_authenticate(user=user)
        url = "/meals/%d/" % meal_id
        client.patch(url, updated_ingredients, format="json")

        new_meal.refresh_from_db()

        self.assertListEqual(updated_ingredients["ingredients"], new_meal.ingredients)
