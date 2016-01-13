from reports import views

__author__ = 'Alexey Kutepov'

from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', views.reports, name="reports"),
)
