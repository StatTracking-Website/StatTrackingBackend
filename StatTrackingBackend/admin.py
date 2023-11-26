from django.contrib import admin

from StatTrackingBackend.models.friendship_models import Friendship, FriendshipRequest
from StatTrackingBackend.models.log_models import Caffeine, TooLate, Horny, CaffeineType, CaffeineCategory, \
    CaffeineCommonServing
from StatTrackingBackend.models.user_models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    pass


@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(CaffeineCategory)
class CaffeineCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(CaffeineType)
class CaffeineTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(CaffeineCommonServing)
class CaffeineCommonAdmin(admin.ModelAdmin):
    pass


@admin.register(Caffeine)
class CaffeineAdmin(admin.ModelAdmin):
    pass


@admin.register(TooLate)
class TooLateAdmin(admin.ModelAdmin):
    pass


@admin.register(Horny)
class HornyAdmin(admin.ModelAdmin):
    pass
