from django.conf.urls import patterns, url

from awards.views import (
    Awards,
    Admin,
    Judging,
    )


urlpatterns = patterns('',
    url(r'^$',
        Awards.as_view(),
        name='list',
        ),
    url(r'^admin/$',
        Admin.as_view(),
        ),
    url(r'^(judging)/$',
        Judging.as_view(),
        name='judging',
        ),
    )
