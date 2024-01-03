from django.db.models import Q
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from StatTrackingBackend.models.friendship_models import FriendshipRequest, Friendship
from StatTrackingBackend.models.user_models import User
from StatTrackingBackend.serializer.friendship_serializer import FriendshipToSerializer, FriendshipFromSerializer, \
    NewFriendshipRequestSerializer, FriendshipSettingsSerializer, FriendshipRequestSerializer, \
    BundledFriendshipSerializer, FriendshipSettingsJoinedSerializer
from StatTrackingBackend.utility import SchwurbelSchema


class APIValueError(APIException):
    status_code = 400
    default_detail = 'Bad Request'
    default_code = 'bad_request'


def catch_error(request):
    try:
        return request()
    except ValueError as e:
        raise APIValueError(detail=str(e))


class FriendshipRequestView(APIView):
    schema = SchwurbelSchema(name='FriendshipRequests')

    def get(self, request):
        if request.query_params.get('type', 'received') == 'sent':
            serializer = FriendshipRequestSerializer(request.user.friendship_requests_sent.all(), many=True, incoming=False)
            return Response(serializer.data)
        serializer = FriendshipRequestSerializer(request.user.friendship_requests_received.all(), many=True, incoming=True)
        return Response(serializer.data)


class NewFriendshipRequestView(APIView):
    schema = SchwurbelSchema(name='newFriendshipRequest', serializer=NewFriendshipRequestSerializer)

    def post(self, request):
        serializer = NewFriendshipRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        catch_error(lambda: FriendshipRequest.objects
                    .request_friendship(user_from=request.user, user_to=data['user_to'], message=data['message']))
        return Response({'detail': 'friendship request was sent'})


class DeclineFriendshipRequestView(APIView):
    schema = SchwurbelSchema(name='declineFriendshipRequest', serializer=FriendshipFromSerializer)

    def post(self, request):
        serializer = FriendshipFromSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        catch_error(lambda: FriendshipRequest.objects
                    .decline_friendship(user_from=data['user_from'], user_to=request.user))
        return Response({'detail': 'friendship request was declined'})


class AcceptFriendshipRequestView(APIView):
    schema = SchwurbelSchema(name='acceptFriendshipRequest', serializer=FriendshipFromSerializer)

    def post(self, request):
        serializer = FriendshipFromSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        catch_error(lambda: FriendshipRequest.objects
                    .accept_friendship(user_from=data['user_from'], user_to=request.user))
        return Response({'detail': 'friendship request was accepted'})


def combine_friendship_requests(request):
    return combine_friendships(request.user.friends, request.user.friends_reversed)


def combine_friendships(friends, friends_access):
    combined = []
    for friend in friends.all():
        friend_access = friends_access.filter(user_to=friend.user_from).first()
        if friend_access:
            combined.append({
                "user": friend.user_to,
                "access_incoming": friend_access.access,
                "access_outgoing": friend.access
            })
    return combined


class BundledFriendshipDataView(APIView):
    # schema = SchwurbelSchema(name='getBundledFriendData', serializer=BundledFriendshipSerializer)

    def get(self, request):
        serializer = BundledFriendshipSerializer({
            "friends": combine_friendship_requests(request),
            "requests_incoming": request.user.friendship_requests_received,
            "requests_outgoing": request.user.friendship_requests_sent
        }, request=request)
        return Response(serializer.data)


class ActiveFriendshipsView(APIView):
    schema = SchwurbelSchema(name='getFriends', serializer=FriendshipSettingsSerializer)

    def get(self, request):
        serializer = FriendshipSettingsJoinedSerializer(combine_friendship_requests(request), many=True)
        return Response(serializer.data)


class UpdateFriendshipView(APIView):
    schema = SchwurbelSchema(name='updateFriendship', serializer=FriendshipSettingsSerializer)

    def put(self, request):
        serializer = FriendshipSettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        (Friendship.objects
         .filter(user_from=request.user, user_to=data['user_to'])
         .update(access=data['access']))
        return Response({'detail': 'friendship was updated'})


class FriendshipRemoveView(APIView):
    schema = SchwurbelSchema(name='removeFriendship', serializer=FriendshipToSerializer)

    def delete(self, request):
        serializer = FriendshipToSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        Friendship.objects.unfriend(user_from=request.user, user_to=data['user_to'])
        return Response({'detail': 'friendship was deleted'})