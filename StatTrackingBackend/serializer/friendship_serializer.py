from rest_framework import serializers

from StatTrackingBackend.models.friendship_models import FriendshipRequest, ACCESS
from StatTrackingBackend.models.user_models import User


class FriendshipRequestSerializer(serializers.ModelSerializer):
    user_to = serializers.SlugRelatedField(slug_field='user_name', queryset=User.objects.all())
    user_from = serializers.SlugRelatedField(slug_field='user_name', queryset=User.objects.all())

    class Meta:
        model = FriendshipRequest
        fields = ['user_from', 'user_to', 'message']


class NewFriendshipRequestSerializer(serializers.ModelSerializer):
    user_to = serializers.SlugRelatedField(slug_field='user_name', queryset=User.objects.all())

    class Meta:
        model = FriendshipRequest
        fields = ['user_to', 'message']


class FriendshipFromSerializer(serializers.Serializer):
    user_from = serializers.SlugRelatedField(slug_field='user_name', queryset=User.objects.all())


class FriendshipToSerializer(serializers.Serializer):
    user_to = serializers.SlugRelatedField(slug_field='user_name', queryset=User.objects.all())


class FriendshipSettingsSerializer(serializers.Serializer):
    user_to = serializers.SlugRelatedField(slug_field='user_name', queryset=User.objects.all())
    access = serializers.MultipleChoiceField(choices=ACCESS)