from meals.models import Meal
from rest_framework import serializers
from accounts.serializers import UserSerializer
from django.contrib.auth.models import User


class MealSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    collaborators = UserSerializer(required=False, many=True)

    def create(self, validated_data):
        collaborator_ids = validated_data.get("collaborators", [])
        collaborators = User.objects.filter(id__in=collaborator_ids)
        new_meal = {k:v for k, v in validated_data.items() if k != "collaborators"}
        meal = Meal(**new_meal)
        meal.save()
        meal.collaborators.set(collaborators)
        return meal

    class Meta:
        model = Meal
        fields = ('pk', 'name', 'owner', 'collaborators', 'taste', 'difficulty', 'last_used', 'used_count', 'notes')