from typing import Type

from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers, status
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from StatTrackingBackend.models import User
from StatTrackingBackend.utility import SchwurbelSchema


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['user_name']


class UserViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50)


class SetPasswordView(APIView):
    queryset = User.objects.all()
    schema = SchwurbelSchema(name='updatePassword', serializer=PasswordSerializer)

    def put(self, request):
        user = request.user
        serializer = PasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({'status': 'password set'})


class RegisterUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['user_name', 'password']


class RegisterUserView(APIView):
    queryset = User.objects.all()
    throttle_scope = 'register_user'
    permission_classes = []
    schema = SchwurbelSchema(name='registerUser', serializer=RegisterUserSerializer)

    def put(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(serializer.validated_data["user_name"], serializer.validated_data["password"])
        return Response({'status': 'user created'})


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=50)


class LoginView(APIView):
    queryset = User.objects.all()
    schema = SchwurbelSchema(name='login', serializer=LoginSerializer)
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=serializer.validated_data["user_name"], password=serializer.validated_data["password"])
        if user is None:
            return Response({'status': status.HTTP_400_BAD_REQUEST})

        login(request, user)
        return Response({'status': 'logged in'})


class LogoutView(APIView):
    permission_classes = []
    schema = SchwurbelSchema(name='logout')

    def post(self, request):
        logout(request)
        return Response({'status': 'logged out'})