from django.contrib import admin
from models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.unregister(User)

class RegistrationProfileInline(admin.TabularInline):
    model = RegistrationProfile
    extra = 0

class CustomUserAdmin(UserAdmin):
    inlines = [RegistrationProfileInline]

    filter_horizontal = ('user_permissions', 'groups')
    save_on_top = True
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')

admin.site.register(User, CustomUserAdmin)

admin.site.register(UserProfile)
admin.site.register(RegistrationProfile)
