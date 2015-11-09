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
        url(r'^get/probationer/list/$', views.get_probationer_list),
        url(r'^get/theme/list/by/user/$', views.get_theme_list_by_user),
        url(r'^get/theme/list/by/journal/$', views.get_theme_list_by_journal),


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
        url(r'^schedule/theme/(?P<id>\d+)/$', views.schedule_theme, name="schedule_theme"),
        url(r'^schedule/theme/to/user/(?P<id>\d+)/$', views.schedule_theme_to_user, name="schedule_theme_to_user"),
        url(r'^user/info/(?P<id>\d+)/$', views.user_info, name="user_info"),
        url(r'^delete/journal/(?P<id>\d+)/$', views.delete_journal, name="delete_journal"),
        url(r'^probationer/theme/settings/(?P<id>\d+)/$', views.probationer_theme_settings, name="probationer_theme_settings"),
        url(r'^theme/in/work/(?P<id>\d+)/$', views.theme_in_work, name="theme_in_work"),
        url(r'^theme/completed/(?P<id>\d+)/$', views.theme_completed, name="theme_completed"),
        url(r'^upload/file/to/sub/theme/$', views.upload_file_to_sub_theme, name="upload_file_to_sub_theme")

)