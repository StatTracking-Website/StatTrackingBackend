from rest_framework import serializers

from StatTrackingBackend.models.friendship_models import FriendshipRequest, ACCESS
from StatTrackingBackend.serializer.user_serializer import UserSlugIdentityField, UserProfileSerializer


class FriendshipRequestSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.fields['user'].source = 'user_from' if kwargs.pop("incoming") else 'user_to'
        super().__init__(*args, **kwargs)

    user = UserProfileSerializer(source='user_to')

    class Meta:
        model = FriendshipRequest
        fields = ['user', 'message']


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


class FriendshipSettingsDetailSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        self.fields['user'].source = 'user_from' if kwargs.pop("incoming") else 'user_to'
        super().__init__(*args, **kwargs)

    user = UserProfileSerializer(source='user_to')
    access = serializers.MultipleChoiceField(choices=ACCESS)


class BundledFriendshipSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.context['request'] = request

    friends = FriendshipSettingsDetailSerializer(many=True, incoming=False)
    friends_access = FriendshipSettingsDetailSerializer(many=True, incoming=True)
    requests_incoming = FriendshipRequestSerializer(many=True, incoming=True)
    requests_outgoing = FriendshipRequestSerializer(many=True, incoming=False)
