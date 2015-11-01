__author__ = 'Alexey Kutepov'

from django.views.generic import TemplateView
from django.conf.urls import patterns, url
from main import views

urlpatterns = patterns('',
        url(r'^test/$', views.test_page, name='test'),
        url(r'^$', views.index, name='index'),

        url(r'^get/department/list/$', views.get_department_list),
        url(r'^get/journal/list/$', views.get_journal_list),
        url(r'^get/user/list/by/department/$', views.get_user_list_by_department),
        url(r'^get/user/list/by/theme/$', views.get_user_list_by_theme),

        url(r'^create/new/company', views.create_new_company, name="create_new_company"),
        url(r'^edit/company/(?P<id>\d+)/$', views.edit_company, name="edit_company"),
        url(r'^edit/company/save/$', views.edit_company_save, name="edit_company_save"),
        url(r'^create/journal/$', views.create_journal, name="create_journal"),
        url(r'^journal/settings/(?P<id>\d+)/$', views.journal_settings, name="journal_settings"),
        url(r'^create/theme/$', views.create_theme, name="create_theme"),
        url(r'^delete/theme/(?P<id>\d+)/$', views.delete_theme, name="delete_theme"),
        url(r'^theme/settings/(?P<id>\d+)/$', views.theme_settings, name="theme_settings"),
        url(r'^create/sub/theme/$', views.create_sub_theme, name="create_sub_theme"),
        url(r'^delete/sub/theme/(?P<id>\d+)/$', views.delete_sub_theme, name="delete_sub_theme"),
)