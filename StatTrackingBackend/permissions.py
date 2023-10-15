from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission

from StatTrackingBackend.models.user_models import User


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = IsAdminUser.has_permission(self, request, view)
        return request.method in SAFE_METHODS or is_admin


class HasAccessRights(BasePermission):
    def has_permission(self, request, view):
        user: User = request.user
        access: str = view.access
        return access in user.access


class PermissionLogSerializer(serializers.Serializer):
    logger = serializers.SlugRelatedField(slug_field='user_name', queryset=User.objects.all())
    person = serializers.SlugRelatedField(slug_field='user_name', queryset=User.objects.all())


class WrongLoggerException(APIException):
    status_code = 400
    default_detail = 'The logger is not the logged-in user'
    default_code = 'wrong_logger'


class IsCorrectLoggerOrReadonly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS: return True

        serializer = PermissionLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['logger'] != request.user:
            raise WrongLoggerException()
        return True


class IsFriendOrReadonly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS: return True

        # Check if the player is a friend of the logged-in user
        serializer = PermissionLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        person: User = serializer.validated_data['person']
        if person == request.user: return True

        access: str = view.access
        return person.friends.filter(Q(user_to=request.user) & Q(access__contains=access)).exists()


