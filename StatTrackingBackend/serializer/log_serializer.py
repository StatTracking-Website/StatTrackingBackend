from rest_framework import serializers

from StatTrackingBackend.models.log_models import Coffee, TooLate, Horny, Log
from StatTrackingBackend.models.user_models import User

log_fields = ['logger', 'time', 'person']


class LogSerializer(serializers.ModelSerializer):
    logger = serializers.SlugRelatedField(slug_field='user_name', queryset=User.objects.all())
    person = serializers.SlugRelatedField(slug_field='user_name', queryset=User.objects.all())


class CoffeeSerializer(LogSerializer):
    class Meta:
        model = Coffee
        fields = log_fields + ['coffee_size', 'coffee_type', 'coffee_source']


class TooLateSerializer(LogSerializer):
    class Meta:
        model = TooLate
        fields = log_fields + ['duration', 'event', 'excuse']


class HornySerializer(LogSerializer):
    class Meta:
        model = Horny
        fields = log_fields + ['assault_target', 'assault_type', 'assault_detail', 'assault_intensity']