from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission

from StatTrackingBackend.models.log_models import TooLate
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


# Check if the player is a friend of the logged-in user
def has_friend_access(person: User, user: User, access: str):
    if person == user: return True
    if person.friends.filter(Q(user_to=user) & Q(access__contains=access)).exists(): return True
    raise PermissionDenied("You are not friends with this person")


class PermissionLogSerializer(serializers.Serializer):
    person = UserSlugIdentityField()


class IsFriendOrReadonly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS: return True

        serializer = PermissionLogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        person: User = serializer.validated_data['person']
        return has_friend_access(person, request.user, view.access)


class PermissionRatingSerializer(serializers.Serializer):
    target = serializers.PrimaryKeyRelatedField(queryset=TooLate.objects.all())


class IsFriendRating(BasePermission):
    def has_object_permission(self, request, view, obj):

        serializer = PermissionRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        person: User = serializer.validated_data['target'].person
        return has_friend_access(person, request.user, view.access)


