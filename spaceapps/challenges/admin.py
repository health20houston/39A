from django.contrib import admin

from .models import (
    Challenge, 
    ChallengeSponsor, 
    ChallengeAuthor,
    Category, 
    ChallengeDataset,
    )


class ChallengeSponsorInline(admin.TabularInline):
    model = ChallengeSponsor
    extra = 1

class ChallengeAuthorInline(admin.TabularInline):
    model = ChallengeAuthor
    extra = 1

class ChallengeDatasetInline(admin.TabularInline):
    model = ChallengeDataset
    extra = 1

class ChallengeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'description')
    inlines = [
        ChallengeSponsorInline,
        ChallengeAuthorInline,
        ChallengeDatasetInline,
        ]

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Category, CategoryAdmin)
