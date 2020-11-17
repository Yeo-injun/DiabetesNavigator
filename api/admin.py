from django.contrib import admin  
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin  
from django.contrib.auth.models import User  

from .models import User_Profile

class Profile_admin(admin.ModelAdmin):
    model = User_Profile
    # exclude = ('user', 'PA')
    list_display = ('user','sex','birthday', 'diabetes_type', 'height', 'weight', 'PA', 'energy_needs')
admin.site.register(User_Profile, Profile_admin)

class ProfileInline(admin.StackedInline):  
    model = User_Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):  
    inlines = (ProfileInline, )
admin.site.unregister(User)  
admin.site.register(User, UserAdmin)