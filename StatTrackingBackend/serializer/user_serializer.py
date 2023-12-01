from rest_framework import serializers

from StatTrackingBackend.models.user_models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=50)
    new_password = serializers.CharField(max_length=50)


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'user_name', 'password']