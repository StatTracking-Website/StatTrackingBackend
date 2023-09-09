from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import serializers
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from StatTrackingBackend.models import Coffee, TooLate, Horny

# GenericViewSet,  # generic view functionality
# CreateModelMixin,  # handles POSTs
# RetrieveModelMixin,  # handles GETs for 1 Company
# UpdateModelMixin,  # handles PUTs and PATCHes
# ListModelMixin # handles GETs for many Companies

log_fields = ['logger', 'time', 'person']


class CoffeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coffee
        fields = log_fields + ['coffee_size', 'coffee_type', 'coffee_source']


class CoffeeViewSet(GenericViewSet, LoginRequiredMixin, PermissionRequiredMixin,
                   CreateModelMixin, RetrieveModelMixin, ListModelMixin):
    permission_required = "StatTrackingBackend.access_coffee"
    serializer_class = CoffeeSerializer
    queryset = Coffee.objects.all()


class TooLateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TooLate
        fields = log_fields + ['duration', 'event', 'excuse']


class TooLateViewSet(GenericViewSet, LoginRequiredMixin, PermissionRequiredMixin,
                   CreateModelMixin, RetrieveModelMixin, ListModelMixin):
    permission_required = "StatTrackingBackend.access_too_late"
    serializer_class = TooLateSerializer
    queryset = TooLate.objects.all()


class HornySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Horny
        fields = log_fields + ['assault_target', 'assault_type', 'assault_detail', 'assault_intensity']


class HornyViewSet(GenericViewSet, LoginRequiredMixin, PermissionRequiredMixin,
                   CreateModelMixin, RetrieveModelMixin, ListModelMixin):
    permission_required = "StatTrackingBackend.access_horny"
    serializer_class = HornySerializer
    queryset = Horny.objects.all()