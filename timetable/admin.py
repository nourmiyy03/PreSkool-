from django.contrib import admin
from .models import TimeTable

@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'student_class', 'day', 'start_time', 'end_time', 'room')
    list_filter = ('day', 'teacher', 'student_class')
    search_fields = ('subject__name', 'teacher__first_name', 'teacher__last_name')