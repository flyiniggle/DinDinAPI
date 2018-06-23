from itertools import chain

from pipetools import pipe
from rest_framework import serializers

from accounts.models import PendingCollaboration
from meals.fields import CollaboratorsField
from meals.models import Meal


class MealSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username', read_only=True)
    collaborators = CollaboratorsField(many=True, required=False)

    def create(self, validated_data):
        '''TODO: don't save collaborators if meal creation fails. Need better error handling'''
        collaborators = self.get_collaborators(validated_data)
        new_meal = self.get_meal_data(validated_data)
        meal = Meal(**new_meal)
        meal.save()

        pending_collaborations = self.create_pending_collaborations(collaborators, meal)

        for collaboration in pending_collaborations:
            collaboration.save()

        return meal

    def update(self, instance, validated_data):
        collaborators = self.get_collaborators(validated_data)
        updated_meal = self.get_meal_data(validated_data)

        pending_collaborations = self.create_pending_collaborations(collaborators, instance)

        for collaboration in pending_collaborations:
            collaboration.save()
        return super().update(instance, updated_meal)

    @staticmethod
    def get_collaborators(meal_data):
        return meal_data.get("collaborators", [])

    @staticmethod
    def get_meal_data(meal_data):
        return {k:v for k, v in meal_data.items() if k != "collaborators"}

    @staticmethod
    def filter_existing_collaborations(collaborator, meal):
        chained_shares = chain(collaborator.shared_meals.all(), collaborator.new_shared_meals.all())
        all_shares = (pipe
                      | list
                      | (map, lambda instance: instance if type(instance) is Meal else instance.meal)
                      | list
                      | (filter, lambda shared_meal: shared_meal.pk == meal.pk)
                      | list
                      )(chained_shares)

        return len(all_shares) == 0

    @staticmethod
    def create_pending_collaborations(collaborations, meal):
        return (pipe
                | (filter, lambda collaborator: MealSerializer.filter_existing_collaborations(collaborator, meal))
                | (map, lambda collaborator: dict(owner=meal.owner, collaborator=collaborator, meal=meal))
                | list
                | (map, lambda c: PendingCollaboration(**c))
                | list
                )(collaborations)

    class Meta:
        model = Meal
        fields = ('pk', 'name', 'owner', 'collaborators', 'taste', 'difficulty', 'last_used', 'used_count', 'notes')
