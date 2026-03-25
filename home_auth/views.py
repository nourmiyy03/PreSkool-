from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role')

        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        # roles
        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'admin':
            user.is_admin = True
        else:
            user.is_student = True

        user.save()
        login(request, user)
        messages.success(request, 'Signup successful!')
        return redirect('student_list')  # 👈 بدل index

    return render(request, 'authentication/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            # redirection
            if user.is_admin:
                return redirect('admin_dashboard')
            elif user.is_teacher:
                return redirect('teacher_dashboard')
            else:
                return redirect('student_list')  # 👈 fix مهم

        else:
            messages.error(request, 'Invalid credentials')
            return redirect('index')

    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')
