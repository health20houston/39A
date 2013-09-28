from django.contrib import admin

from registration.models import (Registration)


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(Registration, RegistrationAdmin)
