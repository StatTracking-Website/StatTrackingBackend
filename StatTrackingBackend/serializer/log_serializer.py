from django.db import models, IntegrityError, transaction
from django.db.models import Avg
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


class TooLateLocalRatingSerializer(serializers.ModelSerializer):
    rater = UserSlugIdentityField()

    class Meta:
        model = TooLateRating
        fields = ("rater", "rating")


class TooLateSerializer(SocialLogSerializer):
    average_rating = serializers.SerializerMethodField()
    ratings = TooLateLocalRatingSerializer(many=True, read_only=True)

    class Meta:
        model = TooLate
        fields = "__all__"

    def get_average_rating(self, obj):
        avg = obj.ratings.aggregate(Avg('rating'))['rating__avg']
        return 0 if avg is None else avg


class TooLateRatingSerializer(serializers.ModelSerializer):
    rater = UserSlugIdentityField()
    target = serializers.PrimaryKeyRelatedField(queryset=TooLate.objects.all())

    class Meta:
        model = TooLateRating
        fields = "__all__"

    def create(self, validated_data):
        try:
            # Attempt to create a new entry
            return super().create(validated_data)
        except IntegrityError:
            with transaction.atomic():
                instance = TooLateRating.objects.select_for_update().get(
                    rater=validated_data['rater'],
                    target=validated_data['target']
                )
                return self.update(instance, validated_data)


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

