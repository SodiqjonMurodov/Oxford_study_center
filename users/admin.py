from django.contrib.auth.models import Group
from django.contrib import admin
from users.models import User, UserConfirmation

admin.site.unregister(Group)
admin.site.register(UserConfirmation)


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'gender', 'date_of_birth', 'phone_number']




    
    