# ViewSets define the view behavior.
from rest_framework import viewsets, serializers
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from StatTrackingBackend.models import User, Coffee, TooLate


# GenericViewSet,  # generic view functionality
# CreateModelMixin,  # handles POSTs
# RetrieveModelMixin,  # handles GETs for 1 Company
# UpdateModelMixin,  # handles PUTs and PATCHes
# ListModelMixin # handles GETs for many Companies

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['user_name', 'rights']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


log_fields = ['person__user_name', 'time', 'logger__user_name']


class CoffeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coffee
        fields = log_fields + ['coffee_size', 'coffee_type', 'coffee_source']


class CoffeeViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, ListModelMixin):
    serializer_class = CoffeeSerializer
    queryset = Coffee.objects.all()


class TooLateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coffee
        fields = log_fields + ['duration', 'event', 'excuse']


class TooLateViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, ListModelMixin):
    serializer_class = TooLateSerializer
    queryset = TooLate.objects.all()


class HornySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coffee
        fields = log_fields + ['assault_target', 'assault_type', 'assault_detail', 'assault_intensity']


class HornyViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, ListModelMixin):
    serializer_class = TooLateSerializer
    queryset = TooLate.objects.all()