from rest_framework import serializers

from StatTrackingBackend.models.log_models import Caffeine, TooLate, Horny, Log, CaffeineType, CaffeineCategory, \
    CaffeineCommonServing
from StatTrackingBackend.models.user_models import User

log_fields = ['logger', 'time', 'person']


class LogSerializer(serializers.ModelSerializer):
    logger = serializers.SlugRelatedField(slug_field='user_name', queryset=User.objects.all())
    person = serializers.SlugRelatedField(slug_field='user_name', queryset=User.objects.all())


class CaffeineSerializer(LogSerializer):
    drink_type = serializers.SlugRelatedField(slug_field='name', queryset=CaffeineType.objects.all())

    class Meta:
        model = Caffeine
        fields = log_fields + ['drink_size', 'drink_type']


class CaffeineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaffeineCategory
        fields = "__all__"


class CaffeineTypeSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", queryset=CaffeineCategory.objects.all())

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


class TooLateSerializer(LogSerializer):
    class Meta:
        model = TooLate
        fields = log_fields + ['duration', 'event', 'excuse']


class HornySerializer(LogSerializer):
    class Meta:
        model = Horny
        fields = log_fields + ['assault_target', 'assault_type', 'assault_detail', 'assault_intensity']