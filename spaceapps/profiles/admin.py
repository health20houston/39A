from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, Background

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )

class BackgroundAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(User)    
admin.site.register(User, UserAdmin)

admin.site.register(Background, BackgroundAdmin)

