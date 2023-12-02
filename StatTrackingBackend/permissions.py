from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission

from StatTrackingBackend.models.user_models import User
from StatTrackingBackend.serializer.user_serializer import UserSlugIdentityField


class IsAdminUserOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = IsAdminUser.has_permission(self, request, view)
        if request.method in SAFE_METHODS or is_admin: return True
        raise PermissionDenied("Admin Permission Required")


class HasAccessRights(BasePermission):
    def has_permission(self, request, view):
        user: User = request.user
        access: str = view.access
        if access in user.access: return True
        raise PermissionDenied("Your account does not has access to this resource")


class PermissionLogSerializer(serializers.Serializer):
    logger = UserSlugIdentityField()
    person = UserSlugIdentityField()


class IsFriendOrReadonly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS: return True

        # Check if the player is a friend of the logged-in user
        serializer = PermissionLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        person: User = serializer.validated_data['person']
        if person == request.user: return True

        access: str = view.access
        if person.friends.filter(Q(user_to=request.user) & Q(access__contains=access)).exists(): return True
        raise PermissionDenied("You are not friends with this person")


