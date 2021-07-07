from django.conf.urls import url

from . import views # import views so we can use them in urls.


urlpatterns = [
    url(r'^$', views.listing, name='listing'),
    url(r'^(?P<albumId>[0-9]+)/$', views.detail, name='detail'),
    url(r'^search/$', views.search, name='search')
]