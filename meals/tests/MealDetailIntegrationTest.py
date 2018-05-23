from django.test import TestCase
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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_text, 'OK')

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
