import coreschema
from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers, status
from rest_framework.decorators import action, schema, permission_classes, api_view
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas.openapi import AutoSchema, SchemaGenerator
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from StatTrackingBackend.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['user_name']


class UserViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50)


class NoPrefixAutoSchema(AutoSchema):

    def __init__(self, name: str):
        AutoSchema.__init__(self, operation_id_base=name)

    method_mapping = {
        'get': '',
        'post': '',
        'put': '',
        'patch': '',
        'delete': '',
    }


class SetPasswordView(APIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordSerializer
    schema = AutoSchema(operation_id_base='Password')

    def put(self, request):
        user = request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=50)


class LoginView(APIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    schema = NoPrefixAutoSchema(name='login')
    permission_classes = []

    def post(self, request):
        username = request.POST["user_name"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'status': 'logged in'})
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST})


class LogoutView(APIView):
    permission_classes = []
    schema = NoPrefixAutoSchema(name='logout')

    def post(self, request):
        logout(request)
        return Response({'status': 'logged out'})