from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from meals.views import MealList
from meals.models import Meal


class MealsTest(TestCase):
    fixtures = ['mealsdump.json', 'authdump.json',]

    def test_get_meals_returns_200_status(self):
        view = MealList.as_view()
        factory = APIRequestFactory()
        request = factory.get('meals', format='json')
        user = User.objects.get(username='test')
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
        user = User.objects.get(username='test')
        force_authenticate(request, user=user)
        response = view(request)
        data = response.data

        for meal in data:
            self.assertIn("name", meal)
            self.assertIn("owner", meal)
            self.assertIn("taste", meal)
            self.assertIn("difficulty", meal)
            self.assertIn("last_used", meal)
            self.assertIn("used_count", meal)
            self.assertIn("notes", meal)

    def test_get_meals_returns_meals_for_specified_user(self):
        view = MealList.as_view()
        factory = APIRequestFactory()
        request = factory.get('meals', format='json')
        user = User.objects.get(username='test')
        force_authenticate(request, user=user)
        response = view(request)
        data = response.data

        for meal in data:
            self.assertEquals(meal.get("owner"), "test")


        user = User.objects.get(username='admin')
        force_authenticate(request, user=user)
        response = view(request)
        data = response.data

        for meal in data:
            self.assertEquals(meal.get("owner"), "admin")

    def test_post_meals_creates_new_meal_entry(self):
        data = {
            "name": "turkey goop",
            "taste": 3,
            "difficulty": 2,
            "last_used": "2018-03-13",
            "used_count": 4,
            "notes": "classic"
        }
        self.client.login(username="test", password="testing123")
        self.client.post("/meals/", data, format="json")
        self.client.logout()
        meal = Meal.objects.filter(name="turkey goop")

        self.assertEqual(len(meal), 1)


    def test_post_meals_associates_meal_with_owner(self):
        data = {
            "name": "turkey goop",
            "taste": 3,
            "difficulty": 2,
            "last_used": "2018-03-13",
            "used_count": 4,
            "notes": "classic"
        }
        self.client.login(username="test", password="testing123")
        self.client.post("/meals/", data, format="json")
        self.client.logout()
        meal = Meal.objects.filter(name="turkey goop")

        self.assertEqual(meal[0].owner, User.objects.get(username="test"))
