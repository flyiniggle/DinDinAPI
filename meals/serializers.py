from meals.models import Meal
from rest_framework import serializers


class MealSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Meal
        fields = ('name', 'owner', 'taste', 'difficulty', 'last_used', 'used_count', 'notes')