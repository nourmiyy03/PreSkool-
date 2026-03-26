from django.urls import path
from . import views


urlpatterns = [
    path('', views.department_list, name='department_list'),
    path('add/', views.department_add, name='department_add'),
    path('edit/<int:department_id>/', views.department_edit, name='department_edit'),
    path('delete/<int:department_id>/', views.department_delete, name='department_delete'),
]