from django.contrib import admin
from main.models import *
from django.contrib.auth.admin import UserAdmin
from main.models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    date_hierarchy = 'date_of_birth'
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'gender',  'company', 'department', 'position', 'registration_date', 'is_staff', 'is_superuser',)
    list_filter = ('gender', 'company', 'department', 'position', 'registration_date', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'middle_name', 'date_of_birth', 'gender', 'photo',)}),
        ('Profile info', {'fields': ('registration_date',)}),
        ('Job info', {'fields': ('company', 'department', 'position',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_active',)}),
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
