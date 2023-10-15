from django.contrib import admin

from StatTrackingBackend.models.friendship_models import Friendship, FriendshipRequest
from StatTrackingBackend.models.log_models import Coffee, TooLate, Horny
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


@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    pass


@admin.register(TooLate)
class TooLateAdmin(admin.ModelAdmin):
    pass


@admin.register(Horny)
class HornyAdmin(admin.ModelAdmin):
    pass
