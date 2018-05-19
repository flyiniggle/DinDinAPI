from meals.models import Meal
from rest_framework import serializers
from meals.fields import CollaboratorsField


class MealSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    collaborators = CollaboratorsField(many=True, required=False)

    def create(self, validated_data):
        collaborators = validated_data.get("collaborators", [])
        new_meal = {k:v for k, v in validated_data.items() if k != "collaborators"}
        meal = Meal(**new_meal)
        meal.save()
        meal.collaborators.set(collaborators)
        return meal

    class Meta:
        model = Meal
        fields = ('pk', 'name', 'owner', 'collaborators', 'taste', 'difficulty', 'last_used', 'used_count', 'notes')