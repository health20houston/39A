from django.contrib import admin

from awards.models import (
	LocalAward, 
	GlobalAwardClass, 
	GlobalAwardFinalist, 
	Nomination,
	)


class NominationAdmin(admin.ModelAdmin):
    list_display = ('project', 'location')

class GlobalAwardClassAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(LocalAward)
admin.site.register(Nomination, NominationAdmin)
admin.site.register(GlobalAwardClass, GlobalAwardClassAdmin)
admin.site.register(GlobalAwardFinalist)
