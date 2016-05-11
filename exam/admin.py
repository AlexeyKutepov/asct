from django.contrib import admin
from exam.models import Test, TestJournal


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'date_and_time')
    list_filter = ('author', 'date_and_time')
    date_hierarchy = 'date_and_time'


@admin.register(TestJournal)
class TestJournalAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'date_from', 'date_to', 'number_of_questions', 'number_of_correct_answers', 'result')
    list_filter = ('user', 'test', 'date_from', 'date_to', 'number_of_questions', 'number_of_correct_answers', 'result')
    date_hierarchy = 'date_to'