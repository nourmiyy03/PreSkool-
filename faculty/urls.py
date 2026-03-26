from django.urls import path
from . import views

urlpatterns = [
path('', views.index, name='index'),
path('dashboard/', views.dashboard, name='dashboard'),
path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('', views.index, name='index'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
]