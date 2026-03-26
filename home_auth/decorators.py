from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(function=None):
    """
    Decorator for views that checks that the logged in user is an admin.
    """
    def check_admin(user):
        return user.is_authenticated and user.is_admin
    
    actual_decorator = user_passes_test(
        check_admin,
        login_url='login',
        redirect_field_name=None
    )
    
    if function:
        return actual_decorator(function)
    return actual_decorator

def teacher_required(function=None):
    """
    Decorator for views that checks that the logged in user is a teacher or admin.
    """
    def check_teacher(user):
        return user.is_authenticated and (user.is_teacher or user.is_admin)
    
    actual_decorator = user_passes_test(
        check_teacher,
        login_url='login',
        redirect_field_name=None
    )
    
    if function:
        return actual_decorator(function)
    return actual_decorator

def student_required(function=None):
    """
    Decorator for views that checks that the logged in user is a student or admin.
    """
    def check_student(user):
        return user.is_authenticated and (user.is_student or user.is_admin)
    
    actual_decorator = user_passes_test(
        check_student,
        login_url='login',
        redirect_field_name=None
    )
    
    if function:
        return actual_decorator(function)
    return actual_decorator

def authorized_required(function=None):
    """
    Decorator for views that checks that the user is authorized (email verified).
    """
    def check_authorized(user):
        return user.is_authenticated and user.is_authorized
    
    actual_decorator = user_passes_test(
        check_authorized,
        login_url='login',
        redirect_field_name=None
    )
    
    if function:
        return actual_decorator(function)
    return actual_decorator