from django.contrib import admin
from users.models import User

@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'gender', 'date_of_birth', 'phone_number']




    
    