from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
import django.contrib.auth.password_validation as validators
from django.core import exceptions

from accounts.models import PendingCollaboration


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])

    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])

    password = serializers.CharField(style={'input_type': 'password'},
                                     write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'])

    def validate_password(self, password):
        user = User(**self.initial_data)

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(password)

    def get(self, request, *args, **kargs):
        return self.retrieve(request)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class PendingCollaborationSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    collaborator = serializers.ReadOnlyField(source='collaborator.username')
    meal = serializers.ReadOnlyField(source='meal.name')

    class Meta:
        model = PendingCollaboration
        fields = ('owner', 'collaborator', 'password')