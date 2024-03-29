import django.contrib.auth.password_validation as validators
from django.contrib.auth.models import User
from django.core import exceptions
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

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

        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))

        return super(UserSerializer, self).validate(password)

    def get(self, request):
        return self.retrieve(request)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class PendingCollaborationSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')
    collaborator_name = serializers.ReadOnlyField(source='collaborator.username')
    meal_name = serializers.ReadOnlyField(source='meal.name')

    class Meta:
        model = PendingCollaboration
        fields = ('owner_name', 'owner', 'collaborator_name', 'collaborator', 'meal_name', 'meal')