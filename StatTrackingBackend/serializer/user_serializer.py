from rest_framework import serializers

from StatTrackingBackend.models.user_models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name']


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=50)
    new_password = serializers.CharField(max_length=50)


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name', 'password']