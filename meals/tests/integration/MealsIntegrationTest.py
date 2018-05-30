from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from meals.models import Meal
from meals.views import MealList


class GetMealsTest(TestCase):
    fixtures = ['dump.json']
    new_meal_data = {
        "name": "turkey goop",
        "taste": 3,
        "difficulty": 2,
        "last_used": "2018-03-13",
        "used_count": 4,
        "notes": "classic"
    }

    def test_get_meals_returns_200_status(self):
        view = MealList.as_view()
        factory = APIRequestFactory()
        request = factory.get('meals', format='json')
        user = User.objects.get(username='test2')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_text, 'OK')

    def test_get_meals_returns_401_status_if_not_logged_in(self):
        view = MealList.as_view()
        factory = APIRequestFactory()
        request = factory.get('meals', format='json')
        response = view(request)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.status_text, 'Unauthorized')

    def test_get_meals_returns_a_meals_list(self):
        view = MealList.as_view()
        factory = APIRequestFactory()
        request = factory.get('meals', format='json')
        user = User.objects.get(username='test2')
        force_authenticate(request, user=user)
        response = view(request)
        data = response.data

        for meal in data:
            with self.subTest(meal=meal):
                self.assertIn("pk", meal)
                self.assertIn("name", meal)
                self.assertIn("owner", meal)
                self.assertIn("collaborators", meal)
                self.assertIn("taste", meal)
                self.assertIn("difficulty", meal)
                self.assertIn("last_used", meal)
                self.assertIn("used_count", meal)
                self.assertIn("notes", meal)

    def test_get_meals_returns_meals_for_specified_user(self):
        view = MealList.as_view()
        factory = APIRequestFactory()
        request = factory.get('meals', format='json')
        user = User.objects.get(username='test1')
        force_authenticate(request, user=user)
        response = view(request)
        data = response.data

        for meal in data:
            with self.subTest(meal=meal):
                is_owner_or_collaborator = (meal.get("owner") == "test1") or user.shared_meals.filter(id=meal.get("pk")).exists()
                self.assertTrue(is_owner_or_collaborator)

        user = User.objects.get(username='admin')
        force_authenticate(request, user=user)
        response = view(request)
        data = response.data

        for meal in data:
            with self.subTest(meal=meal):
                is_owner_or_collaborator = (meal.get("owner") == "admin") or user.shared_meals.filter(id=meal.get("pk")).exists()
                self.assertTrue(is_owner_or_collaborator)


class CreateMealsTest(TestCase):
    fixtures = ['dump.json']
    new_meal_data = {
        "name": "turkey goop",
        "taste": 3,
        "difficulty": 2,
        "last_used": "2018-03-13",
        "used_count": 4,
        "notes": "classic"
    }

    def test_post_meals_returns_201_status(self):
        view = MealList.as_view()
        factory = APIRequestFactory()
        request = factory.post('meals', self.new_meal_data, format='json')
        user = User.objects.get(username='test1')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.status_text, 'Created')

    def test_post_meals_returns_401_status_if_not_logged_in(self):
        view = MealList.as_view()
        factory = APIRequestFactory()
        request = factory.post('meals', self.new_meal_data, format='json')
        response = view(request)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.status_text, 'Unauthorized')

    def test_post_meals_creates_new_meal_entry(self):
        self.client.login(username="test1", password="testing123")
        self.client.post("/meals/", self.new_meal_data, format="json")
        self.client.logout()
        meal = Meal.objects.filter(name="turkey goop")

        self.assertEqual(len(meal), 1)

    def test_post_meals_associates_meal_with_owner(self):
        self.client.login(username="test2", password="testing123")
        self.client.post("/meals/", self.new_meal_data, format="json")
        self.client.logout()
        meal = Meal.objects.filter(name="turkey goop")

        self.assertEqual(meal[0].owner, User.objects.get(username="test2"))

    def test_post_meals_saves_form_data(self):
        self.client.login(username="test1", password="testing123")
        self.client.post("/meals/", self.new_meal_data, format="json")
        self.client.logout()
        meal = Meal.objects.get(name="turkey goop")

        date_used = datetime.strptime(self.new_meal_data.get("last_used"), "%Y-%m-%d").date()

        self.assertEqual(meal.name, self.new_meal_data.get("name"))
        self.assertEqual(meal.taste, self.new_meal_data.get("taste"))
        self.assertEqual(meal.difficulty, self.new_meal_data.get("difficulty"))
        self.assertEqual(meal.last_used, date_used)
        self.assertEqual(meal.used_count, self.new_meal_data.get("used_count"))
        self.assertEqual(meal.notes, self.new_meal_data.get("notes"))

    def test_post_meals_notes_are_optional(self):
        data = {key:self.new_meal_data[key] for key in self.new_meal_data if key != "notes"}
        self.client.login(username="test1", password="testing123")
        self.client.post("/meals/", data, format="json")
        self.client.logout()
        meal = Meal.objects.get(name="turkey goop")

        date_used = datetime.strptime(self.new_meal_data.get("last_used"), "%Y-%m-%d").date()

        self.assertEqual(meal.name, self.new_meal_data.get("name"))
        self.assertEqual(meal.taste, self.new_meal_data.get("taste"))
        self.assertEqual(meal.difficulty, self.new_meal_data.get("difficulty"))
        self.assertEqual(meal.last_used, date_used)
        self.assertEqual(meal.used_count, self.new_meal_data.get("used_count"))
        self.assertEqual(meal.notes, "")

    def test_post_meals_creates_a_meal_with_used_count_of_0(self):
        data = {key:self.new_meal_data[key] for key in self.new_meal_data if key != "used_count"}
        self.client.login(username="test1", password="testing123")
        self.client.post("/meals/", data, format="json")
        self.client.logout()
        meal = Meal.objects.get(name=self.new_meal_data["name"])

        self.assertEqual(meal.used_count, 0)

    def test_post_meals_creates_a_meal_with_no_last_used_date(self):
        data = {key:self.new_meal_data[key] for key in self.new_meal_data if key != "last_used"}
        self.client.login(username="test1", password="testing123")
        self.client.post("/meals/", data, format="json")
        self.client.logout()
        meal = Meal.objects.get(name=self.new_meal_data["name"])

        self.assertIsNone(meal.last_used)
