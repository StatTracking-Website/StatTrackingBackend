from django.contrib import admin

from StatTrackingBackend.models import Coffee, TooLate, Horny, User


@admin.register(User)
class CoffeeAdmin(admin.ModelAdmin):
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
