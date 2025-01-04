from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'room')
    search_fields = ('username', 'email', 'room')

admin.site.register(User, CustomUserAdmin)

