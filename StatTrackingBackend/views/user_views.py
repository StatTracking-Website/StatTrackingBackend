from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from StatTrackingBackend.email import send_confirm_email
from StatTrackingBackend.filters import SpecificUsersFilter
from StatTrackingBackend.models.user_models import User, UserVerification, UserProfile
from StatTrackingBackend.serializer.user_serializer import UserProfileSerializer, RegisterUserSerializer, \
    UpdatePasswordSerializer, UserSerializer, find_user_from_identity
from StatTrackingBackend.utility import SchwurbelSchema, LateThrottleAPIView, generate_random_string, \
    check_required_keys


class UserViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SpecificUsersFilter]
    serializer_class = UserProfileSerializer


class ProfilePictureUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.profile.picture = request.data['file']
        request.user.profile.save()


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


class ResetPasswordView(LateThrottleAPIView):
    throttle_scope = 'reset_password'
    permission_classes = [AllowAny]

    def post(self, request):
        check_required_keys(request.data, ['email'])
        user: User = get_object_or_404(User, email=request.data['email'])

        self.check_throttles(request)

        confirm_code = generate_random_string(50)
        try:
            user.verification.password_code = confirm_code
            user.verification.save()
        except UserVerification.DoesNotExist:
            UserVerification.objects.create(user=user, password_code=confirm_code)

        send_confirm_email(user.email, user.user_name, confirm_code)
        return Response({'detail': 'reset email was sent'})


class RegisterUserView(LateThrottleAPIView):
    throttle_scope = 'register_user'
    permission_classes = [AllowAny]
    schema = SchwurbelSchema(name='registerUser', serializer=RegisterUserSerializer)

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.check_throttles(request)
        data = serializer.validated_data

        confirm_code = generate_random_string(10)
        user: User = User.objects.create_user(data['email'], data["user_name"], data["password"])
        UserVerification.objects.create(user=user, email_code=confirm_code)
        send_confirm_email(data['email'], data['user_name'], confirm_code)
        return Response({'detail': 'user created'})


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        check_required_keys(request.data, ['code', 'identity'])
        user: User = find_user_from_identity(request.data['identity'])
        if user.verification.email_code != request.data["code"]:
            return Response({'detail': 'code not valid'}, status=status.HTTP_400_BAD_REQUEST)

        user.verification.verified_email = True
        user.verification.save()
        return Response({'detail': 'email verified'})


class FinalizePasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        check_required_keys(request.data, ['code', 'new_password', 'identity'
                                           ])
        user: User = find_user_from_identity(request.data['identity'])
        if user.verification.password_code != request.data["code"]:
            return Response({'detail': 'code not valid'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(request.data["new_password"])
        user.save()
        return Response({'detail': 'password reset'})


class TokenVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        verification = UserVerification.objects.get_or_create(user=request.user)[0]
        profile = UserProfile.objects.get_or_create(user=request.user)[0]
        return Response(
            {
                'detail': 'token is working',
                'uuid': request.user.uuid,
                'user_name': request.user.user_name,
                'email': request.user.email,
                'access': request.user.access,
                'verified': verification.verified_email,
                'profile_picture': request.build_absolute_uri(profile.picture.url) if profile.picture else '',
                'profile_bio': profile.bio
            })
