__author__ = 'Alexey Kutepov'

from django.conf.urls import patterns, url
from exam import views

urlpatterns = patterns('',
        url(r'^create/new/test/', views.create_new_test, name='create_new_test'),
        url(r'^test/settings/(?P<id>\d+)/$', views.test_settings, name='test_settings'),
        url(r'^create/new/question/(?P<id>\d+)/$', views.create_new_question, name='create_new_question'),
        url(r'^edit/test/(?P<id>\d+)/$', views.edit_test, name='edit_test'),
        url(r'^delete/test/(?P<id>\d+)/$', views.delete_test, name='delete_test'),
        url(r'^cancel/test/(?P<id>\d+)/$', views.cancel_test, name='cancel_test'),
        url(r'^add/question/(?P<id>\d+)/$', views.add_question, name='add_question'),
        url(r'^edit/question/(?P<id>\d+)/(?P<number>\d+)/$', views.edit_question, name='edit_question'),
        url(r'^delete/question/(?P<id>\d+)/$', views.delete_question, name='delete_question'),
        url(r'^schedule/test/(?P<id>\d+)/$', views.schedule_test, name="schedule_test"),
        url(r'^schedule/test/to/user/$', views.schedule_test_to_user),
        url(r'^edit/scheduled/test/(?P<id>\d+)/$', views.edit_scheduled_test, name="edit_scheduled_test"),
        url(r'^test/(?P<id>\d+)/$', views.start_test, name='start_test'),
        url(r'^next/question/(?P<id>\d+)/(?P<number>\d+)/$', views.next_question, name='next_question'),
        url(r'^end/test/(?P<id>\d+)/$', views.end_test, name='end_test'),
        url(r'^report/(?P<id>\d+)/$', views.report, name='report'),
)