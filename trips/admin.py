from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import Trip, User

from rest_framework_api_key.admin import APIKeyModelAdmin
from .models import UserAPIKey

@admin.register(UserAPIKey)
class OrganizationAPIKeyModelAdmin(APIKeyModelAdmin):
    pass



@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    pass


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    fields = (
        'id', 'pick_up_address', 'drop_off_address', 'status', 'image',
        'driver', 'rider',
        'created', 'updated',
    )
    list_display = (
        'id', 'pick_up_address', 'drop_off_address', 'status', 'image',
        'driver', 'rider',
        'created', 'updated',
    )
    list_filter = (
        'status',
    )
    readonly_fields = (
        'id', 'created', 'updated',
    )
