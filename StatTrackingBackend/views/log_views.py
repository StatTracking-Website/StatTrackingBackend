from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from StatTrackingBackend.filters import IsFriendFilter, LogTimeFilter, LogTimeWindowFilter, LogTargetFilter
from StatTrackingBackend.models.log_models import Caffeine, TooLate, CaffeineType, CaffeineCategory, \
    CaffeineCommonServing, TooLateRating, Sleep, Money, MoneyUseCase
from StatTrackingBackend.permissions import IsFriendOrReadonly, HasAccessRights, IsFriendRating
from StatTrackingBackend.serializer.log_serializer import TooLateSerializer, CaffeineSerializer, \
    CaffeineTypeSerializer, BundledCaffeineSortSerializer, TooLateRatingSerializer, SleepSerializer, MoneySerializer, \
    MoneyUseCaseSerializer


class BaseLogViewSet(GenericAPIView, ListModelMixin, CreateModelMixin):
    def get(self, request, *args, **kwargs): return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs): return self.create(request, *args, **kwargs)


class SocialLogViewSet(BaseLogViewSet):
    def initial(self, request, *args, **kwargs):
        request.data['logger'] = request.user.user_name
        super().initial(request, *args, **kwargs)


class LogViewSet(BaseLogViewSet):
    def initial(self, request, *args, **kwargs):
        request.data['person'] = request.user.user_name
        super().initial(request, *args, **kwargs)


class CaffeineTypeViewSet(RetrieveAPIView):
    serializer_class = BundledCaffeineSortSerializer
    permission_classes = [IsAuthenticated, HasAccessRights]
    access = 'Caffeine'

    def get_object(self): return {
        "categories": CaffeineCategory.objects.all(),
        "types": CaffeineType.objects.all(),
        "common_serving": CaffeineCommonServing.objects.all()
    }


class CaffeineViewSet(SocialLogViewSet):
    serializer_class = CaffeineSerializer
    queryset = Caffeine.objects.all()
    permission_classes = [IsAuthenticated, HasAccessRights, IsFriendOrReadonly]
    filter_backends = [IsFriendFilter, LogTimeFilter, LogTimeWindowFilter, LogTargetFilter]
    access = 'Caffeine'


class TooLateRatingViewSet(CreateAPIView):
    serializer_class = TooLateRatingSerializer
    queryset = TooLateRating.objects.all()
    permission_classes = [IsAuthenticated, HasAccessRights, IsFriendRating]
    access = 'TooLate'


class TooLateViewSet(SocialLogViewSet):
    serializer_class = TooLateSerializer
    queryset = TooLate.objects.all()
    permission_classes = [IsAuthenticated, HasAccessRights, IsFriendOrReadonly]
    filter_backends = [IsFriendFilter, LogTimeFilter, LogTimeWindowFilter, LogTargetFilter]
    access = 'TooLate'


class SleepViewSet(LogViewSet):
    serializer_class = SleepSerializer
    queryset = Sleep.objects.all()
    permission_classes = [IsAuthenticated, HasAccessRights, IsFriendOrReadonly]
    filter_backends = [IsFriendFilter, LogTimeFilter, LogTimeWindowFilter, LogTargetFilter]
    access = 'Sleep'


class MoneyUseCaseViewSet(RetrieveAPIView):
    serializer_class = MoneyUseCaseSerializer
    queryset = MoneyUseCase.objects.all()
    permission_classes = [IsAuthenticated, HasAccessRights]
    access = 'Money'
    exclude_from_schema = True


class MoneyViewSet(LogViewSet):
    serializer_class = MoneySerializer
    queryset = Money.objects.all()
    permission_classes = [IsAuthenticated, HasAccessRights, IsFriendOrReadonly]
    filter_backends = [IsFriendFilter, LogTimeFilter, LogTimeWindowFilter, LogTargetFilter]
    access = 'Money'
    exclude_from_schema = True

