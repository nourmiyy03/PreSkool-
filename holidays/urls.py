from django.urls import path
from . import views

urlpatterns = [
    path('', views.holiday_list, name='holiday_list'),
    path('calendar/', views.holiday_calendar, name='holiday_calendar'),
    path('add/', views.add_holiday, name='add_holiday'),
    path('edit/<int:holiday_id>/', views.edit_holiday, name='edit_holiday'),
    path('delete/<int:holiday_id>/', views.delete_holiday, name='delete_holiday'),
]