from django.contrib import admin
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    pass



# Register your models here.
#admin.site.register(User)