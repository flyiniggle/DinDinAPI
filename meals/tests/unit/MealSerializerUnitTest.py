from django.contrib.auth.models import User
from django.test import TestCase
from pipetools import pipe

from accounts.models import PendingCollaboration
from meals.models import Meal
from meals.serializers import MealSerializer


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


class MealSerializerCreatePendingCollaborationTest(TestCase):
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


class MealSerializerFilterExistingCollaborationsTest(TestCase):
    fixtures = ['dump.json']
    new_meal_data = {
        "name": "turkey goop",
        "taste": 3,
        "difficulty": 2,
        "last_used": "2018-03-13",
        "used_count": 4,
        "notes": "classic"
    }
    pending_collaborators_data = [2, 3]
    existing_collaborators_data = [1]

    def test_filter_existing_collaborations_returns_false_if_collaboration_exists(self):
        new_meal = Meal(**self.new_meal_data)
        new_meal.save()
        owner = User.objects.get(id=4)
        for collaborator in self.pending_collaborators_data:
            user = User.objects.get(id=collaborator)
            PendingCollaboration(meal=new_meal, collaborator=user, owner=owner).save()

        new_meal.collaborators.set(self.existing_collaborators_data)
        collaborator = User.objects.get(id=self.existing_collaborators_data[0])

        self.assertFalse(MealSerializer.filter_existing_collaborations(collaborator, new_meal))

    def test_filter_existing_collaborations_returns_false_if_pending_collaboration_exists(self):
        new_meal = Meal(**self.new_meal_data)
        new_meal.save()
        new_meal.collaborators.set(self.pending_collaborators_data)
        owner = User.objects.get(id=4)
        for collaborator in self.pending_collaborators_data:
            user = User.objects.get(id=collaborator)
            PendingCollaboration(meal=new_meal, collaborator=user, owner=owner).save()

        collaborator = User.objects.get(id=self.pending_collaborators_data[0])
        include_in_list = MealSerializer.filter_existing_collaborations(collaborator, new_meal)

        self.assertFalse(include_in_list)

    def test_filter_existing_collaborations_returns_true_if_no_collaboration_exists(self):
        new_meal = Meal(**self.new_meal_data)
        new_meal.save()
        collaborator = User.objects.get(id=self.pending_collaborators_data[0])
        include_in_list = MealSerializer.filter_existing_collaborations(collaborator, new_meal)

        self.assertTrue(include_in_list)
