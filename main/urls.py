__author__ = 'Alexey Kutepov'

from django.views.generic import TemplateView
from django.conf.urls import patterns, url
from main import views

urlpatterns = patterns('',
        url(r'^test/$', views.test_page, name='test'),
        url(r'^$', views.index, name='index'),
        url(r'^get/department/list/$', views.get_department_list),
        url(r'^/get/user/list/by/department/$', views.get_user_list_by_department)
)