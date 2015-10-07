__author__ = 'Alexey Kutepov'

from django.views.generic import TemplateView
from django.conf.urls import patterns, url
from main import views

urlpatterns = patterns('',
        url(r'^test/$', views.test_page, name='test'),
        url(r'^user/settings/(?P<id>\d+)/$', views.user_settings, name='user_settings'),
        url(r'^$', views.index, name='index'),
)