from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view

from StatTrackingBackend.views.friendship_views import NewFriendshipRequestView, DeclineFriendshipRequestView, \
    AcceptFriendshipRequestView, UpdateFriendshipView, ActiveFriendshipsView, FriendshipRemoveView, \
    FriendshipRequestView, BundledFriendshipDataView
from StatTrackingBackend.views.log_views import CaffeineViewSet, TooLateViewSet, CaffeineTypeViewSet, \
    TooLateRatingViewSet, SleepViewSet, MoneyViewSet, MoneyUseCaseViewSet
from StatTrackingBackend.views.user_views import UserViewSet, SetPasswordView, RegisterUserView, TokenVerifyView, \
    ResetPasswordView, ConfirmEmailView, FinalizePasswordResetView, ProfilePictureUploadView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', get_schema_view(
        title='Stat Tracking Backend',
        description='''An API to access all data tracked by the stat tracking system''',
        permission_classes=[AllowAny],
        public=True,
    ), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc-ui'),

    path('users/upload-profile-picture/', ProfilePictureUploadView.as_view(), name="upload_profile_picture"),
    path('users/set-password/', SetPasswordView.as_view(), name="set_password"),
    path('users/reset-password/', ResetPasswordView.as_view(), name="reset_password"),
    path('users/register-user/', RegisterUserView.as_view(), name="register_user"),

    path('users/hidden/confirm-email/', ConfirmEmailView.as_view(), name="confirm_email"),
    path('users/hidden/reset-password/', FinalizePasswordResetView.as_view(), name="confirm_email"),

    path('friends/bundled-data/', BundledFriendshipDataView.as_view(), name="bundled_friendship"),
    path('friends/', ActiveFriendshipsView.as_view(), name="friendships"),
    path('friends/update/', UpdateFriendshipView.as_view(), name="update_friendship"),
    path('friends/remove/', FriendshipRemoveView.as_view(), name="remove_friendship"),
    path('friends/requests/', FriendshipRequestView.as_view(), name="friendship_requests"),
    path('friends/requests/new/', NewFriendshipRequestView.as_view(), name="new_friendship_requests"),
    path('friends/requests/decline/', DeclineFriendshipRequestView.as_view(), name="decline_friendship_requests"),
    path('friends/requests/accept/', AcceptFriendshipRequestView.as_view(), name="accept_friendship_requests"),


    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('logs/caffeine/', CaffeineViewSet.as_view(), name="coffee"),
    path('logs/caffeine/types/', CaffeineTypeViewSet.as_view(), name="coffee_types"),
    path('logs/too_late/ratings/', TooLateRatingViewSet.as_view(), name="too_late_ratings"),
    path('logs/too_late/', TooLateViewSet.as_view(), name="too_late"),
    path('logs/sleep/', SleepViewSet.as_view(), name="sleep"),
    path('logs/money/use-case/', MoneyUseCaseViewSet.as_view(), name="money_use_case"),
    path('logs/money/', MoneyViewSet.as_view(), name="money"),

    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
