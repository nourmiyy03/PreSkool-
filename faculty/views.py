from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from student.models import Student
from holidays.models import Holiday
from datetime import datetime
# from teachers.models import Teacher  # À décommenter quand Personne 1 crée l'app teachers
# from exams.models import Exam, Result  # À décommenter quand on crée l'app exams


def index(request):
    return render(request, 'authentication/login.html')


@login_required
def dashboard(request):
    """Redirection vers le dashboard selon le rôle"""
    user = request.user
    
    if user.is_admin:
        return redirect('admin_dashboard')
    elif user.is_teacher:
        return redirect('teacher_dashboard')
    elif user.is_student:
        return redirect('student_dashboard')
    else:
        return redirect('index')


@login_required
def admin_dashboard(request):
    """Dashboard pour l'administrateur"""
    user = request.user
    
    # Vérifier que l'utilisateur est admin
    if not user.is_admin and not user.is_superuser:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('student_list')
    
    # Statistiques
    total_students = Student.objects.count()
    # total_teachers = Teacher.objects.count()  # À décommenter plus tard
    total_holidays = Holiday.objects.count()
    upcoming_holidays = Holiday.objects.filter(start_date__gte=datetime.now().date()).count()
    
    # Derniers étudiants ajoutés
    recent_students = Student.objects.all().order_by('-id')[:5]
    
    # Prochains jours fériés
    next_holidays = Holiday.objects.filter(start_date__gte=datetime.now().date()).order_by('start_date')[:5]
    
    context = {
        'total_students': total_students,
        # 'total_teachers': total_teachers,
        'total_holidays': total_holidays,
        'upcoming_holidays': upcoming_holidays,
        'recent_students': recent_students,
        'next_holidays': next_holidays,
        'user': user,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def teacher_dashboard(request):
    """Dashboard pour l'enseignant"""
    user = request.user
    
    # Vérifier que l'utilisateur est enseignant
    if not user.is_teacher and not user.is_admin:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('student_list')
    
    context = {
        'user': user,
    }
    
    return render(request, 'dashboard/teacher_dashboard.html', context)


@login_required
def student_dashboard(request):
    """Dashboard pour l'étudiant"""
    user = request.user
    
    # Vérifier que l'utilisateur est étudiant
    if not user.is_student and not user.is_admin:
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('student_list')
    
    # Récupérer l'étudiant lié à l'utilisateur (si connecté)
    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        student = None
    
    # Prochains jours fériés
    upcoming_holidays = Holiday.objects.filter(start_date__gte=datetime.now().date()).order_by('start_date')[:3]
    
    context = {
        'user': user,
        'student': student,
        'upcoming_holidays': upcoming_holidays,
    }
    
    return render(request, 'dashboard/student_dashboard.html', context)


