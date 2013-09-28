from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView

from django.conf import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^selectable/', include('selectable.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('core.urls')),

    # url(r'^messages/', include('postman.urls')),
    # url(r'^notifications?/', include('notification.urls')),
    
    url(r'^account/', include('allauth.urls')),
    url(r'^challenges?/', include('challenges.urls', namespace='challenges')),
    url(r'^locations?/', include('locations.urls', namespace='locations')),
    url(r'^register/', include('registration.urls', namespace='registration')),
    url(r'^projects?/', include('projects.urls', namespace='projects')),
    url(r'^profiles?/', include('profiles.urls', namespace='profiles')),
    url(r'^awards?/', include('awards.urls', namespace='awards')),
)

urlpatterns += i18n_patterns('',
    url(r'^$', TemplateView, { 'template': 'home.html' }),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
