from django.db import models
from rest_framework import serializers

from StatTrackingBackend.models.log_models import Caffeine, TooLate, Log, CaffeineType, CaffeineCategory, \
    CaffeineCommonServing, TooLateRating, Sleep, MoneyUseCase, Money
from StatTrackingBackend.serializer.user_serializer import UserSlugIdentityField


class LogSerializer(serializers.ModelSerializer):
    person = UserSlugIdentityField()


class SocialLogSerializer(LogSerializer):
    logger = UserSlugIdentityField()


class CaffeineSerializer(SocialLogSerializer):
    drink_type = serializers.SlugRelatedField(slug_field='name', queryset=CaffeineType.objects.all())

    class Meta:
        model = Caffeine
        fields = "__all__"


class CaffeineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaffeineCategory
        fields = "__all__"


class CaffeineTypeSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=CaffeineCategory.objects.all())

    class Meta:
        model = CaffeineType
        fields = "__all__"


class CaffeineCommonServingSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaffeineCommonServing
        fields = "__all__"


class BundledCaffeineSortSerializer(serializers.Serializer):
    categories = CaffeineCategorySerializer(many=True)
    types = CaffeineTypeSerializer(many=True)
    common_serving = CaffeineCommonServingSerializer(many=True)


class RatingField(serializers.Field):
    def to_representation(self, obj): return obj.ratings_received.all().aggregate(models.Avg('rating'))['rating__avg']


class TooLateSerializer(SocialLogSerializer):
    rating = RatingField(read_only=True)

    class Meta:
        model = TooLate
        fields = "__all__"


class TooLateRatingSerializer(serializers.ModelSerializer):
    rater = UserSlugIdentityField()
    target = serializers.PrimaryKeyRelatedField(queryset=TooLate.objects.all())

    class Meta:
        model = TooLateRating
        fields = "__all__"


class SleepSerializer(LogSerializer):
    class Meta:
        model = Sleep
        fields = "__all__"


class MoneyUseCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoneyUseCase
        fields = "__all__"


class MoneySerializer(LogSerializer):
    class Meta:
        model = Money
        fields = "__all__"

