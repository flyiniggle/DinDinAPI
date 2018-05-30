from django.test import TestCase
from pipetools import pipe

from meals.serializers import MealSerializer
from meals.models import Meal
from django.contrib.auth.models import User


class MealSerializeTest(TestCase):
    def test_get_collaborators_returns_collaborators(self):
        test_data = {
            "collaborators": [1, 2, 3],
            "otherdata": "this is more data"
        }

        result = MealSerializer.get_collaborators(test_data)

        self.assertEqual(result, [1, 2, 3])

    def test_get_collaborators_returns_empty_list(self):
        test_data = {
            "otherdata": "this is more data"
        }

        result = MealSerializer.get_collaborators(test_data)

        self.assertEqual(result, [])

    def test_get_meal_data_returns_meal_without_collaborators(self):
        test_data = {
            "collaborators": [1, 2, 3],
            "otherdata": "this is more data"
        }

        result = MealSerializer.get_meal_data(test_data)

        self.assertEqual(result, {"otherdata": "this is more data"})
        self.assertNotIn("collaborators", result)

    def test_create_pending_collaborations(self):
        user = User()
        user.save()
        collaborators = (pipe
                         | list
                         | (filter, lambda x: user is x)
                         | list
                         | (lambda col: col[0:2]))(User.objects.all())

        meal = Meal(name="test",
                    taste=1,
                    owner=user,
                    difficulty=5)
        meal.save()

        pending_collaborations = MealSerializer.create_pending_collaborations(collaborators, meal)
        for collaboration in pending_collaborations:
            with self.subTest(collaboration=collaboration):
                self.assertEqual(collaboration, meal)
