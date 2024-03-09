from rest_framework import serializers


from StatTrackingBackend.models.user_models import User, UserProfile


def find_user_from_identity(data):
    if User.objects.filter(email=data).exists():
        return User.objects.get(email=data)
    elif User.objects.filter(user_name=data).exists():
        return User.objects.get(user_name=data)
    elif User.objects.filter(uuid=data).exists():
        return User.objects.get(uuid=data)
    else:
        raise serializers.ValidationError("User not found")


class UserIdentityField(serializers.Field):
    def to_representation(self, obj): return obj.user_name
    def to_internal_value(self, data): return find_user_from_identity(data)


class UserSlugIdentityField(serializers.RelatedField):

    def __init__(self, **kwargs): super().__init__(queryset=User.objects.all(), **kwargs)
    def to_representation(self, obj): return obj.user_name
    def to_internal_value(self, data): return find_user_from_identity(data)


class UserSerializer(serializers.ModelSerializer):
    identity = UserIdentityField(source='*')

    class Meta:
        model = User
        fields = ['identity']


class UserProfileSerializer(serializers.ModelSerializer):
    identity = UserIdentityField(source='*')
    profile_picture = serializers.ImageField(source='profile.picture', use_url=True)
    profile_bio = serializers.CharField(source='profile.bio')

    class Meta:
        model = User
        fields = ['identity', 'profile_picture', 'profile_bio']


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'user_name', 'password']


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=50)
    new_password = serializers.CharField(max_length=50)


