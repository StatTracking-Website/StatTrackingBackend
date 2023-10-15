from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from django.db.models import Q, QuerySet
from django.utils import timezone
from rest_framework import filters
from rest_framework.exceptions import APIException
from rest_framework.request import Request

from StatTrackingBackend.models.user_models import User


def is_friend_and_has_access(user, access):
    return Q(person__friends__user_to=user) & Q(person__friends__access__contains=access)


class IsFriendFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset: QuerySet, view):
        user: User = request.user
        access = view.access
        return (queryset.prefetch_related('person__friends')
                .filter(Q(person=user) | is_friend_and_has_access(user, access)))


class MalformedTimeException(APIException):
    status_code = 400
    default_detail = 'Malformed time unit (minutes, hours, days, weeks, months, years)'
    default_code = 'malformed_unit'


class MalformedIntException(APIException):
    status_code = 400
    default_detail = 'Couldn\'t parse Integer, please enter a valid Number'
    default_code = 'malformed_int'


class LogTimeFilter(filters.BaseFilterBackend):

    @staticmethod
    def get_mapping(key: str, amount: int):
        return relativedelta(**{key: amount})

    def filter_queryset(self, request, queryset, view):
        request: Request = request
        unit = request.query_params.get('unit', 'days')
        size = request.query_params.get('size', '1')
        offset = request.query_params.get('offset', '0')

        try:
            size = int(size)
            offset = int(offset)
            relative_delta = self.get_mapping(unit, size)
            offset = self.get_mapping(unit, offset)
            return (queryset.filter(time__gte=timezone.now() - relative_delta - offset)
                    .filter(time__lte=timezone.now() - offset))
        except ValueError:
            raise MalformedIntException()
        except TypeError:
            raise MalformedTimeException()


class MalformedDateTimeException(APIException):
    status_code = 400
    default_detail = 'Malformed date time (%Y/%m/%dT%H:%M:%SZ) => (2019-08-24T14:15:22Z)'
    default_code = 'malformed_unit'


class LogTimeWindowFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        request: Request = request
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        if not start_time: return queryset

        try:
            start_time = datetime.strptime(start_time, "%Y/%m/%dT%H:%M:%SZ")
            end_time = datetime.strptime(end_time, "%Y/%m/%dT%H:%M:%SZ") if end_time else timezone.now()
            return queryset.filter(Q(time__gte=start_time) & Q(time__lte=end_time))
        except ValueError:
            raise MalformedDateTimeException()


class UserDoesNotExistException(APIException):
    status_code = 400
    default_detail = 'Requested user does not exist'
    default_code = 'user_does_not_exist'


class LogUserFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        request: Request = request
        target_person = request.query_params.get('user')
        if not target_person: target_person = request.query_params.get('person')
        if not target_person: return queryset

        try:
            target_person = User.objects.get(user_name=target_person)
            return queryset.filter(person=target_person)
        except User.DoesNotExist:
            raise UserDoesNotExistException()
