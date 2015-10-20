from django.contrib import admin
from main.models import *
from django.contrib.auth.admin import UserAdmin
from main.models import UserProfile


@admin.register(Company)
class Company(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)

@admin.register(Department)
class Department(admin.ModelAdmin):
    list_display = ('name', 'company')
    list_filter = ('name', 'company')


@admin.register(SubThemeResult)
class SubThemeResult(admin.ModelAdmin):
    list_display = ('result', 'user', 'date', 'sub_theme_exam')
    list_filter = ('result', 'user', 'date', 'sub_theme_exam')


@admin.register(SubThemeExam)
class SubThemeExam(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner', 'sub_theme')
    list_filter = ('name', 'description', 'owner', 'sub_theme')


@admin.register(ScheduledSubTheme)
class ScheduledSubTheme(admin.ModelAdmin):
    list_display = ('date_from', 'date_to', 'user', 'sub_theme')
    list_filter = ('date_from', 'date_to', 'user', 'sub_theme')


@admin.register(SubTheme)
class SubTheme(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner', 'parent_theme')
    list_filter = ('name', 'description', 'owner', 'parent_theme')


@admin.register(ThemeResult)
class ThemeResult(admin.ModelAdmin):
    list_display = ('result', 'user', 'date', 'theme_exam')
    list_filter = ('result', 'user', 'date', 'theme_exam')


@admin.register(ThemeExam)
class ThemeExam(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner', 'theme')
    list_filter = ('name', 'description', 'owner', 'theme')


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


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    date_hierarchy = 'date_of_birth'
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'gender',  'company', 'department', 'position', 'registration_date', 'user_type', 'is_staff', 'is_superuser',)
    list_filter = ('gender', 'company', 'department', 'position', 'registration_date', 'user_type', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'middle_name', 'date_of_birth', 'gender', 'photo',)}),
        ('Profile info', {'fields': ('registration_date',)}),
        ('Job info', {'fields': ('company', 'department', 'position',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'user_type',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
