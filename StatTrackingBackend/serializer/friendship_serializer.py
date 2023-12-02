from rest_framework import serializers

from StatTrackingBackend.models.friendship_models import FriendshipRequest, ACCESS
from StatTrackingBackend.serializer.user_serializer import UserSlugIdentityField


class FriendshipRequestSerializer(serializers.ModelSerializer):
    user_to = UserSlugIdentityField()
    user_from = UserSlugIdentityField()

    class Meta:
        model = FriendshipRequest
        fields = ['user_from', 'user_to', 'message']


class NewFriendshipRequestSerializer(serializers.ModelSerializer):
    user_to = UserSlugIdentityField()

    class Meta:
        model = FriendshipRequest
        fields = ['user_to', 'message']


class FriendshipFromSerializer(serializers.Serializer):
    user_from = UserSlugIdentityField()


class FriendshipToSerializer(serializers.Serializer):
    user_to = UserSlugIdentityField()


class FriendshipSettingsSerializer(serializers.Serializer):
    user_to = UserSlugIdentityField()
    access = serializers.MultipleChoiceField(choices=ACCESS)


class ReverseFriendshipSettingsSerializer(serializers.Serializer):
    user_from = UserSlugIdentityField()
    access = serializers.MultipleChoiceField(choices=ACCESS)


class BundledFriendshipSerializer(serializers.Serializer):
    friends = FriendshipSettingsSerializer(many=True)
    friends_access = ReverseFriendshipSettingsSerializer(many=True)
    requests_incoming = FriendshipRequestSerializer(many=True)
    requests_outgoing = FriendshipRequestSerializer(many=True)
