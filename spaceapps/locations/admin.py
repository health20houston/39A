from django.contrib import admin

from .models import Location, Sponsor, Lead, Resource


class SponsorInline(admin.TabularInline):
    model = Sponsor
    extra = 1

class LeadInline(admin.TabularInline):
    model = Lead
    extra = 1

class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1

class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'city', 'country', 'capacity',)
    inlines = [
        SponsorInline,
        LeadInline,
        ResourceInline,
        ]

admin.site.register(Location, LocationAdmin)