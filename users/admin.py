from django.contrib.auth.models import Group
from django.contrib import admin
from users.models import User, UserConfirmation

admin.site.unregister(Group)


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'gender', 'date_of_birth', 'phone_number']


@admin.register(UserConfirmation)
class UserConfirmationModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'user', 'expiration_time', 'is_confirmed']

    fieldsets = (
        (None, {
            'fields': ('code', 'user', 'expiration_time', 'is_confirmed')
        }),
    )

