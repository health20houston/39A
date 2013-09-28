from django.conf.urls import patterns, url

from .views import (
    Detail, 
    List, 
    Create, 
    Edit,
    Delete)


urlpatterns = patterns('',
    url(r'^$',
        List.as_view(),
        name='list_challenges'),
    url(r'^create/$',
        Create.as_view(),
        ),
    url(r'^(?P<slug>[-_\w]+)/$',
        Detail.as_view(),
        name='view_challenge',
        ),
    url(r'^(?P<slug>[-_\w]+)/edit$',
        Edit.as_view(),
        ),
    url(r'^(?P<slug>[-_\w]+)/delete$',
        Delete.as_view(),
        ),
    )
