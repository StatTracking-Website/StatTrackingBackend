from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from StatTrackingBackend.filters import IsFriendFilter, LogTimeFilter, LogTimeWindowFilter, LogUserFilter
from StatTrackingBackend.models.log_models import Coffee, TooLate, Horny
from StatTrackingBackend.permissions import IsFriendOrReadonly, IsCorrectLoggerOrReadonly, HasAccessRights
from StatTrackingBackend.serializer.log_serializer import HornySerializer, TooLateSerializer, CoffeeSerializer


class LogViewSet(GenericAPIView, ListModelMixin, CreateModelMixin):
    def get(self, request, *args, **kwargs): return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs): return self.create(request, *args, **kwargs)


class CoffeeViewSet(LogViewSet):
    serializer_class = CoffeeSerializer
    queryset = Coffee.objects.all()
    permission_classes = [IsAuthenticated, HasAccessRights, IsCorrectLoggerOrReadonly, IsFriendOrReadonly]
    filter_backends = [IsFriendFilter, LogTimeFilter, LogTimeWindowFilter, LogUserFilter]
    access = 'Coffee'


class TooLateViewSet(LogViewSet):
    serializer_class = TooLateSerializer
    queryset = TooLate.objects.all()
    permission_classes = [IsAuthenticated, HasAccessRights, IsCorrectLoggerOrReadonly, IsFriendOrReadonly]
    filter_backends = [IsFriendFilter, LogTimeFilter, LogTimeWindowFilter, LogUserFilter]
    access = 'TooLate'


class HornyViewSet(LogViewSet):
    serializer_class = HornySerializer
    queryset = Horny.objects.all()
    permission_classes = [IsAuthenticated, HasAccessRights, IsCorrectLoggerOrReadonly, IsFriendOrReadonly]
    filter_backends = [IsFriendFilter, LogTimeFilter, LogTimeWindowFilter, LogUserFilter]
    exclude_from_schema = True
    access = 'Horny'
