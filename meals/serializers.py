from meals.models import Meal
from rest_framework import serializers


class MealSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Meal
        fields = ('name', 'taste', 'difficulty', 'last_used', 'used_count', 'notes')