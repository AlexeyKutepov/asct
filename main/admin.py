from django.contrib import admin
from main.models import *
from django.contrib.auth.admin import UserAdmin
from authentication.models import UserProfile


@admin.register(Company)
class Company(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)

@admin.register(Department)
class Department(admin.ModelAdmin):
    list_display = ('name', 'company')
    list_filter = ('name', 'company')


@admin.register(ScheduledSubTheme)
class ScheduledSubTheme(admin.ModelAdmin):
    list_display = ('date_from', 'date_to', 'user', 'sub_theme')
    list_filter = ('date_from', 'date_to', 'user', 'sub_theme')


@admin.register(SubTheme)
class SubTheme(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner', 'parent_theme')
    list_filter = ('name', 'description', 'owner', 'parent_theme')


@admin.register(ThemeExam)
class ThemeExam(admin.ModelAdmin):
    list_display = ('user', 'examiner', 'theme', 'datetime', 'place', 'result')
    list_filter = ('user', 'examiner', 'theme', 'datetime', 'place', 'result')


@admin.register(ScheduledTheme)
class ScheduledTheme(admin.ModelAdmin):
    list_display = ('date_from', 'date_to', 'user', 'theme')
    list_filter = ('date_from', 'date_to', 'user', 'theme')


@admin.register(Theme)
class Theme(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner', 'journal')
    list_filter = ('name', 'description', 'owner', 'journal')


@admin.register(Journal)
class Journal(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner')
    list_filter = ('name', 'description', 'owner')


@admin.register(File)
class File(admin.ModelAdmin):
    list_display = ('file', 'theme', 'sub_theme')
    list_filter = ('file', 'theme', 'sub_theme')

