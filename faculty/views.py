from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from home_auth.decorators import admin_required, teacher_required, student_required


def index(request):
    """Redirect to login page if not authenticated, otherwise to appropriate dashboard"""
    if request.user.is_authenticated:
        # User is logged in, redirect to their dashboard
        if request.user.is_admin:
            return redirect('admin_dashboard')
        elif request.user.is_teacher:
            return redirect('teacher_dashboard')
        elif request.user.is_student:
            return redirect('student_dashboard')
        else:
            # Fallback
            return redirect('login')
    else:
        # User not logged in, redirect to login page
        return redirect('login')

@login_required
@admin_required
def admin_dashboard(request):
    try:
        from teachers.models import Teacher
        from departments.models import Department
        from subjects.models import Subject
        from student.models import Student
        
        context = {
            'total_teachers': Teacher.objects.count(),
            'total_departments': Department.objects.count(),
            'total_subjects': Subject.objects.count(),
            'total_students': Student.objects.count(),
            'user': request.user,
        }
    except:
        context = {
            'total_teachers': 0,
            'total_departments': 0,
            'total_subjects': 0,
            'total_students': 0,
            'user': request.user,
        }
    
    # Utiliser un template existant ou créer un template admin
    # Option 1: Créer un nouveau template admin-dashboard.html dans Home/
    return render(request, 'Home/admin-dashboard.html', context)

@login_required
@teacher_required
def teacher_dashboard(request):
    try:
        from teachers.models import Teacher
        from subjects.models import Subject
        
        try:
            teacher = Teacher.objects.get(user=request.user)
            subjects = Subject.objects.filter(teacher=teacher)
        except Teacher.DoesNotExist:
            teacher = None
            subjects = []
        
        context = {
            'teacher': teacher,
            'subjects': subjects,
            'user': request.user,
        }
    except:
        context = {
            'teacher': None,
            'subjects': [],
            'user': request.user,
        }
    
    # Pour l'enseignant, on peut utiliser student-dashboard.html modifié ou en créer un
    return render(request, 'students/teacher-dashboard.html', context)

@login_required
@student_required
def student_dashboard(request):
    try:
        from student.models import Student
        
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = None
        
        context = {
            'student': student,
            'user': request.user,
        }
    except Exception as e:
        context = {
            'student': None,
            'user': request.user,
        }
    
    return render(request, 'students/student-dashboard.html', context)