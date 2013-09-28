from django.conf.urls import patterns, url

from registration.views import (
    List,
    Create,
    Edit,
    Delete,
    )


urlpatterns = patterns('',
    url(r'^$',
        List.as_view(),
        name='base',
        ),
    url(r'^edit/$',
        Edit.as_view(),
        name="edit",
        ),
    url(r'^delete/$',
        Delete.as_view(),
        name='delete',
        ),
    url(r'^(?P<slug>[-_\w]+)/$',
        Create.as_view(),
        name='register',
        ),
    )
