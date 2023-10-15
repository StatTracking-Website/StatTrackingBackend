from rest_framework import serializers, status, permissions
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from StatTrackingBackend.models.user_models import User
from StatTrackingBackend.serializer.user_serializer import UserSerializer, RegisterUserSerializer, \
    UpdatePasswordSerializer
from StatTrackingBackend.utility import SchwurbelSchema, LateThrottleAPIView


class UserViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class SetPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    schema = SchwurbelSchema(name='updatePassword', serializer=UpdatePasswordSerializer)

    def put(self, request):
        user = request.user
        serializer = UpdatePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"detail": "Old Password not Valid!"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'password set'})


class RegisterUserView(LateThrottleAPIView):
    throttle_scope = 'register_user'
    permission_classes = [AllowAny]
    schema = SchwurbelSchema(name='registerUser', serializer=RegisterUserSerializer)

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.check_throttles(request)
        User.objects.create_user(serializer.validated_data["user_name"], serializer.validated_data["password"])
        return Response({'detail': 'user created'})


class VerifyTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(
            {
                'status': 'token is working',
                'user_name': request.user.user_name,
                'access': request.user.access,
            })
