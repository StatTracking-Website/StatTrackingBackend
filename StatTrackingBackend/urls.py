"""
URL configuration for StatTrackingBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from StatTrackingBackend.views.log_views import CoffeeViewSet, TooLateViewSet, HornyViewSet
from StatTrackingBackend.views.user_views import UserViewSet, SetPasswordView, LoginView, LogoutView, RegisterUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('coffee', CoffeeViewSet)
router.register('too_late', TooLateViewSet)
router.register('horny', HornyViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', get_schema_view(
        title='Stat Tracking Backend',
        description='''An API to access all data tracked by the stat tracking system'''
    ), name='openapi-schema'),
    path('docs/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc-ui'),

    path('users/setPassword/', SetPasswordView.as_view(), name="set_password"),
    path('users/registerUser', RegisterUserView.as_view(), name="register_user"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
