__author__ = 'Alexey Kutepov'

from django.conf.urls import patterns, url
from authentication import views

urlpatterns = patterns('',
        url(r'^login/$', views.login, name='login'),
        url(r'^logout/$', views.logout, name='logout'),
        url(r'^settings/(?P<id>\d+)/$', views.user_settings, name='user_settings'),
        # url(r'^create/profile/$', views.create_profile, name='create_profile'),
        # url(r'^settings/$', views.settings, name='settings'),
        # url(r'^recovery/password/$', views.recovery_password, name='recovery_password'),
        # url(r'^alert/(?P<status>.+)/(?P<message>.+)/$', views.alert, name='authentication_alert'),
)
