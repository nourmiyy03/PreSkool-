from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .decorators import admin_required, teacher_required, student_required

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back {user.first_name or user.username}!')
            
            # Redirection selon le rôle
            if user.is_admin:
                return redirect('admin_dashboard')
            elif user.is_teacher:
                return redirect('teacher_dashboard')
            elif user.is_student:
                return redirect('student_dashboard')
            else:
                return redirect('index')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'authentication/login.html')

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role', 'student')
        
        # Vérifier que les mots de passe correspondent
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'authentication/register.html')
        
        # Vérifier si l'utilisateur existe déjà
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'authentication/register.html')
        
        # Créer l'utilisateur
        user = CustomUser.objects.create_user(
            username=email,  # Utiliser l'email comme username
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        
        # Assigner le rôle
        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'admin':
            user.is_admin = True
        
        # Optionnel : marquer comme autorisé si pas besoin de validation email
        user.is_authorized = True
        
        user.save()
        
        # Connecter automatiquement l'utilisateur
        login(request, user)

        messages.success(request, 'Signup successful!')
        
        # Redirection après inscription selon le rôle

        messages.success(request, 'Account created successfully!')
        
        # Redirection selon le rôle

        if user.is_admin:
            return redirect('admin_dashboard')
        elif user.is_teacher:
            return redirect('teacher_dashboard')

        else:
            return redirect('student_dashboard')  
    return render(request, 'authentication/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            # redirection selon le rôle
            if user.is_admin or user.is_superuser:
                return redirect('admin_dashboard')
            elif user.is_teacher:
                return redirect('teacher_dashboard')
            elif user.is_student:
                return redirect('student_dashboard')  
            else:
                # Par défaut, rediriger vers student_dashboard
                return redirect('student_dashboard')


        else:
            return redirect('student_dashboard')
    
    return render(request, 'authentication/register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')