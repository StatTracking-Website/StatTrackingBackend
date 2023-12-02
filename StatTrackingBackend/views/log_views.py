from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from StatTrackingBackend.filters import IsFriendFilter, LogTimeFilter, LogTimeWindowFilter, LogTargetFilter
from StatTrackingBackend.models.log_models import Caffeine, TooLate, Horny, CaffeineType, CaffeineCategory, \
    CaffeineCommonServing
from StatTrackingBackend.permissions import IsFriendOrReadonly, HasAccessRights
from StatTrackingBackend.serializer.log_serializer import HornySerializer, TooLateSerializer, CaffeineSerializer, \
    CaffeineTypeSerializer, BundledCaffeineSortSerializer


class LogViewSet(GenericAPIView, ListModelMixin, CreateModelMixin):
    def get(self, request, *args, **kwargs): return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs): return self.create(request, *args, **kwargs)

    def initial(self, request, *args, **kwargs):
        request.data['logger'] = request.user.user_name
        super().initial(request, *args, **kwargs)


class CaffeineTypeViewSet(RetrieveAPIView):
    serializer_class = BundledCaffeineSortSerializer

    def get_object(self): return {
        "categories": CaffeineCategory.objects.all(),
        "types": CaffeineType.objects.all(),
        "common_serving": CaffeineCommonServing.objects.all()
    }


class CaffeineViewSet(LogViewSet):
    serializer_class = CaffeineSerializer
    queryset = Caffeine.objects.all()
    permission_classes = [IsAuthenticated, HasAccessRights, IsFriendOrReadonly]
    filter_backends = [IsFriendFilter, LogTimeFilter, LogTimeWindowFilter, LogTargetFilter]
    access = 'Caffeine'


class TooLateViewSet(LogViewSet):
    serializer_class = TooLateSerializer
    queryset = TooLate.objects.all()
    permission_classes = [IsAuthenticated, HasAccessRights, IsFriendOrReadonly]
    filter_backends = [IsFriendFilter, LogTimeFilter, LogTimeWindowFilter, LogTargetFilter]
    access = 'TooLate'


class HornyViewSet(LogViewSet):
    serializer_class = HornySerializer
    queryset = Horny.objects.all()
    permission_classes = [IsAuthenticated, HasAccessRights, IsFriendOrReadonly]
    filter_backends = [IsFriendFilter, LogTimeFilter, LogTimeWindowFilter, LogTargetFilter]
    exclude_from_schema = True
    access = 'Horny'
