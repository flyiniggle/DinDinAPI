from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase, force_authenticate

from accounts.models import PendingCollaboration
from accounts.views import UserCollaborations
from meals.models import Meal
from meals.serializers import MealSerializer
from meals.views import MealList


class CreateCollaboration(APITestCase):
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

    def test_add_pending_collaborator_on_meal_creation(self):
        '''
        Create a new meal with collaborators. The collaborators should result in new pending collaborations
        being created.
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

        self.assertIsNotNone(PendingCollaboration.objects.get(collaborator=collaborator1, meal=meal))
        self.assertIsNotNone(PendingCollaboration.objects.get(collaborator=collaborator2, meal=meal))

    def test_add_collaboration_to_existing_meal(self):
        '''
        Add collaborators to an existing meal. The collaborators should result in new pending collaborations
        being created.
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

    def test_add_existing_collaboration_to_meal_fails(self):
        client = APIClient()
        meal_data = MealSerializer.get_meal_data(self.new_meal_data)
        collaborators_data = MealSerializer.get_collaborators(self.new_meal_data)
        meal = Meal(**meal_data)
        meal.save()
        meal.collaborators.set(collaborators_data)
        meal_id = meal.pk
        meal_owner = meal.owner.username
        user = User.objects.get(username=meal_owner)
        client.force_authenticate(user=user)
        url = "/meals/%d/" % meal_id
        client.patch(url, {"collaborators": [2]}, format="json")
        collaborator = User.objects.get(id=2)
        new_collaboration_exists = collaborator.new_shared_meals.filter(meal=meal).exists()

        self.assertFalse(new_collaboration_exists)


class GetCollaboration(APITestCase):
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

    def test_get_pending_collaborations_returns_200(self):
        view = UserCollaborations.as_view()
        factory = APIRequestFactory()
        request = factory.get("user/pending")
        user = User.objects.get(username='admin')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_pending_collaborations_returns_401_if_user_is_unauthenticated(self):
        view = UserCollaborations.as_view()
        factory = APIRequestFactory()
        request = factory.get("user/pending")
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_pending_collaborations_returns_list_of_pending_shared_meals_for_user(self):
        view = UserCollaborations.as_view()
        factory = APIRequestFactory()
        request = factory.get("user/pending")
        user = User.objects.get(username='admin')
        force_authenticate(request, user=user)
        response = view(request)

        pending_meals = PendingCollaboration.objects.filter(collaborator=user)
        for pending_collaboration in response.data:
            with self.subTest(pending_collaboration=pending_collaboration):
                self.assertIsNotNone(pending_meals.filter(meal=pending_collaboration["meal"]))


class UpdateCollaboration(APITestCase):
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

    def test_accept_collaboration(self):
        client = self.client
        user = User.objects.get(username='test1')
        meal = PendingCollaboration.objects.get(pk=1).meal
        client.force_authenticate(user=user)
        url = reverse("accounts:edit-pending-collaboration", kwargs={"id": 1})
        response = client.patch(url, {"accept": True}, format="json")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue(user.shared_meals.filter(id=meal.id).exists())

    def test_accepct_collaboration_fails_if_not_logged_in(self):
        client = self.client
        user = User.objects.get(username='test1')
        meal = PendingCollaboration.objects.get(pk=1).meal
        url = reverse("accounts:edit-pending-collaboration", kwargs={"id": 1})
        response = client.patch(url, {"accept": True}, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(user.shared_meals.filter(id=meal.id).exists())
        self.assertTrue(PendingCollaboration.objects.filter(pk=1).exists())

    def test_accept_collaboration_removes_pending_collaboration(self):
        pending_collaboration = PendingCollaboration.objects.get(pk=1)
        client = self.client
        user = User.objects.get(username='test1')
        client.force_authenticate(user=user)
        url = reverse("accounts:edit-pending-collaboration", kwargs={"id": 1})
        client.patch(url, {"accept": True}, format="json")

        self.assertFalse(PendingCollaboration.objects.filter(meal=pending_collaboration.meal, collaborator=user.pk).exists())

    def test_decline_collaboration(self):
        client = self.client
        user = User.objects.get(username='test1')
        meal = PendingCollaboration.objects.get(pk=1).meal
        client.force_authenticate(user=user)
        url = reverse("accounts:edit-pending-collaboration", kwargs={"id": 1})
        response = client.patch(url, {"accept": False}, format="json")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertFalse(user.shared_meals.filter(id=meal.id).exists())

    def test_decline_collaboration_removes_pending_collaboration(self):
        pending_collaboration = PendingCollaboration.objects.get(pk=1)
        client = self.client
        user = User.objects.get(username='test1')
        client.force_authenticate(user=user)
        url = reverse("accounts:edit-pending-collaboration", kwargs={"id": 1})
        client.patch(url, {"accept": False}, format="json")

        self.assertFalse(PendingCollaboration.objects.filter(meal=pending_collaboration.meal, collaborator=user.pk).exists())


class DeleteUpdateCollaboration(APITestCase):
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

    def test_owner_remove_collaborator_from_existing_meal(self):
        pass

    def test_collaborator_remove_self_from_existing_meal(self):
        pass
