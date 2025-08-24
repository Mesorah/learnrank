from django.contrib import admin

from authors.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'change_username_data']
    # readonly_fields = ['change_username_data']
    fields = [
        'username', 'email', 'change_username_data',
        'is_active', 'is_staff'
    ]
