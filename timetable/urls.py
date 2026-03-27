from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable_by_class, name='timetable_by_class'),
    path('by-class/<int:class_id>/', views.timetable_by_class, name='timetable_by_class_with_id'),
    path('by-teacher/', views.timetable_by_teacher, name='timetable_by_teacher'),
    path('by-teacher/<int:teacher_id>/', views.timetable_by_teacher, name='timetable_by_teacher_with_id'),
    path('add/', views.add_timetable, name='add_timetable'),
    path('edit/<int:timetable_id>/', views.edit_timetable, name='edit_timetable'),
    path('delete/<int:timetable_id>/', views.delete_timetable, name='delete_timetable'),
]