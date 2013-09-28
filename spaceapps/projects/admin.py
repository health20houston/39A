from django.contrib import admin

from .models import (Project, License, Team, Resource)


class TeamInline(admin.TabularInline):                               
    model = Team 
    extra = 1

class ResourceInline(admin.TabularInline):                              
    model = Resource 
    extra = 1

class ProjectAdmin(admin.ModelAdmin):                                         
    prepopulated_fields = {'slug': ('title',)}                                  
    list_display = ('title', 'description')
    inlines = [                                                                 
        TeamInline,                                                  
        ResourceInline,
    ]

admin.site.register(Project, ProjectAdmin)
admin.site.register(License)
