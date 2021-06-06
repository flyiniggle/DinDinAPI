from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class CollaboratorsField(serializers.PrimaryKeyRelatedField):
    queryset = User.objects.all()

    def to_representation(self, value):
        return value.pk

    def to_internal_value(self, data):
        try:
            return User.objects.get(pk=data)
        except ObjectDoesNotExist:
            return None
