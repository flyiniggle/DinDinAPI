from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from meals.views import MealList


class MealsTest(TestCase):
    fixtures = ['mealsdump.json', 'authdump.json']

    def test_get_meals_returns_200_status(self):
        view = MealList.as_view()
        factory = APIRequestFactory()
        request = factory.get('meals', format='json')
        user = User.objects.get(username='test')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_text, 'OK')

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