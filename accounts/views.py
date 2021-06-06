from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from rest_framework import authentication, generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from accounts.models import PendingCollaboration
from accounts.serializers import PendingCollaborationSerializer, UserSerializer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(instance=None, created=False, **kwargs):
    """Generate a token whenever a user is created"""
    if created:
        Token.objects.create(user=instance)


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (authentication.TokenAuthentication,)


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
    queryset = User.objects.all()
    lookup_field = "id"


class UserCollaborations(generics.ListAPIView, generics.UpdateAPIView):
    serializer_class = PendingCollaborationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return PendingCollaboration.objects.filter(collaborator=user)

    def update(self, request, *args, **kwargs):
        collaboration = self.get_queryset().filter(id=kwargs["id"]).first()
        accepted = request.data.get("accept", False)

        if accepted:
            collaboration.meal.collaborators.add(collaboration.collaborator)

        collaboration.delete()

        return Response(status=status.HTTP_202_ACCEPTED)