__author__ = 'Alexey Kutepov'

from django.conf.urls import patterns, url
from authentication import views

urlpatterns = patterns('',
        url(r'^login/$', views.login, name='login'),
        url(r'^logout/$', views.logout, name='logout'),
        url(r'^settings/(?P<id>\d+)/$', views.user_settings, name='user_settings'),
        url(r'^create/new/user/$', views.create_new_user, name='create_new_user'),
        url(r'^give/new/password/(?P<id>\d+)$', views.give_new_password, name='give_new_password'),
        url(r'^delete/user/(?P<id>\d+)$', views.delete_user, name='delete_user'),
        url(r'^fire/user/(?P<id>\d+)$', views.fire_user, name='fire_user'),
)
