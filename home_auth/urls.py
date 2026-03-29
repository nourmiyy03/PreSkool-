from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
path('signup/', views.signup_view, name='signup'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
path('profile/', views.profile_view, name='profile'),
path('forgot-password/', auth_views.PasswordResetView.as_view(), name='forgot-password'),
  path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='authentication/change_password.html',
        success_url='/authentication/password-change-done/'
    ), name='change_password'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'
    ), name='password_change_done'),
]