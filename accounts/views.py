from rest_framework import generics, permissions
from accounts.serializers import UserSerializer, PendingCollaborationSerializer
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Generate a token whenever a user is created"""
    if created:
        Token.objects.create(user=instance)


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()


class UserProfile(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()

    def get_object(self):
        user = self.request.user
        obj = get_object_or_404(self.get_queryset(), username=user.username)
        self.check_object_permissions(self.request, obj)
        return obj


class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), id=self.kwargs["id"])
        self.check_object_permissions(self.request, obj)
        return obj


class UserCollaborations(generics.ListAPIView):
    serializer_class = PendingCollaborationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        self.request.user
        return []

