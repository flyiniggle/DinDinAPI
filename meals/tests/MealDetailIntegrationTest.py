from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient
from django.contrib.auth.models import User
from meals.views import MealDetail
from meals.models import Meal


class MealDetailTest(TestCase):
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

    def test_update_meal(self):
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
        client.patch(url, updated_data, format="json")
        meal.refresh_from_db()

        self.assertEqual(meal.name, updated_data["name"])
        self.assertEqual(meal.taste, updated_data["taste"])
        self.assertEqual(meal.difficulty, updated_data["difficulty"])
        self.assertEqual(meal.notes, updated_data["notes"])

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

        self.assertEqual(meal["name"], updated_data["name"])
        self.assertEqual(meal["taste"], updated_data["taste"])
        self.assertEqual(meal["difficulty"], updated_data["difficulty"])
        self.assertEqual(meal["notes"], updated_data["notes"])

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
