from django.conf.urls import patterns, url

from .views import (
    Home,
    Error,
    Lost,
    No,
    )


urlpatterns = patterns('',
    url(r'^$',
        Home.as_view(),
        ),
    url(r'^500$',
        Error.as_view(),
        ),
    url(r'^404$',
        Lost.as_view(),
        ),
    url(r'^403$',
        No.as_view(),
        ),
    )
