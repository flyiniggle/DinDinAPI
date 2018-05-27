from meals.models import Meal
from rest_framework import serializers
from meals.fields import CollaboratorsField
from accounts.models import PendingCollaboration


class MealSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username', read_only=True)
    collaborators = CollaboratorsField(many=True, required=False, read_only=True)

    def create(self, validated_data):
        collaborators = validated_data.get("collaborators", [])
        new_meal = {k:v for k, v in validated_data.items() if k != "collaborators"}
        meal = Meal(**new_meal)
        meal.save()

        pending_collaborations_args = list(map(lambda collaborator: dict(
            owner=new_meal['owner'],
            collaborator=collaborator,
            meal=meal), collaborators))

        pending_collaborations = list(map(lambda collaboration: PendingCollaboration(**collaboration),
                                          pending_collaborations_args))

        for collaboration in pending_collaborations:
            collaboration.save()

        return meal

    class Meta:
        model = Meal
        fields = ('pk', 'name', 'owner', 'collaborators', 'taste', 'difficulty', 'last_used', 'used_count', 'notes')
