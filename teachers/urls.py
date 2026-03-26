from django.urls import path
from . import views


urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),
    path('add/', views.teacher_add, name='teacher_add'),
    path('view/<int:teacher_id>/', views.teacher_view, name='teacher_view'),
    path('edit/<int:teacher_id>/', views.teacher_edit, name='teacher_edit'),
    path('delete/<int:teacher_id>/', views.teacher_delete, name='teacher_delete'),
]