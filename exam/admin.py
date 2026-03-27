from django.contrib import admin
from .models import Exam, Result

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'date', 'duration', 'room', 'coefficient')
    list_filter = ('subject', 'date')
    search_fields = ('title', 'subject__name')
    date_hierarchy = 'date'

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'score', 'created_at')
    list_filter = ('exam', 'student')
    search_fields = ('student__first_name', 'student__last_name', 'exam__title')