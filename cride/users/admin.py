from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from cride.users.models import User, Profile


class CustomUserAdmin(UserAdmin):
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name', 'is_staff', 'is_client', 'is_verified')
    list_display_links = ('pk', )
    list_editable = ('is_verified',)
    list_filter = ('is_client', 'is_staff', 'created', 'modified')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reputation', 'rides_taken', 'rides_offered')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('reputation',)


admin.site.register(User, CustomUserAdmin)
