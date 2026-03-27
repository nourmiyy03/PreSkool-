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
        from exam.models import Exam          # ← AJOUTER
        from holidays.models import Holiday    # ← AJOUTER
        
        context = {
            'total_teachers': Teacher.objects.count(),
            'total_departments': Department.objects.count(),
            'total_subjects': Subject.objects.count(),
            'total_students': Student.objects.count(),
            'total_exams': Exam.objects.count(),        # ← AJOUTER
            'total_holidays': Holiday.objects.count(),  # ← AJOUTER
            'user': request.user,
        }
    except:
        context = {
            'total_teachers': 0,
            'total_departments': 0,
            'total_subjects': 0,
            'total_students': 0,
            'total_exams': 0,        # ← AJOUTER
            'total_holidays': 0,     # ← AJOUTER
            'user': request.user,
        }
    
    return render(request, 'Home/admin-dashboard.html', context)


@login_required
@teacher_required
def teacher_dashboard(request):
    try:
        from teachers.models import Teacher
        from subjects.models import Subject
        from exam.models import Exam          # ← AJOUTER (optionnel)
        from holidays.models import Holiday    # ← AJOUTER (optionnel)
        
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
            'total_exams': Exam.objects.count(),        # ← AJOUTER (optionnel)
            'total_holidays': Holiday.objects.count(),  # ← AJOUTER (optionnel)
        }
    except:
        context = {
            'teacher': None,
            'subjects': [],
            'user': request.user,
            'total_exams': 0,
            'total_holidays': 0,
        }
    
    return render(request, 'students/teacher-dashboard.html', context)


@login_required
@student_required
def student_dashboard(request):
    try:
        from student.models import Student
        from exam.models import Result   # ← AJOUTER pour les notes
        from holidays.models import Holiday  # ← AJOUTER
        
        try:
            student = Student.objects.get(user=request.user)
            # Récupérer les notes de l'étudiant
            results = Result.objects.filter(student=student).select_related('exam')[:5]
            total_results = results.count()
        except Student.DoesNotExist:
            student = None
            results = []
            total_results = 0
        
        context = {
            'student': student,
            'user': request.user,
            'results': results,           # ← AJOUTER
            'total_results': total_results,  # ← AJOUTER
            'total_holidays': Holiday.objects.count(),  # ← AJOUTER
        }
    except Exception as e:
        context = {
            'student': None,
            'user': request.user,
            'results': [],
            'total_results': 0,
            'total_holidays': 0,
        }
    
    return render(request, 'students/student-dashboard.html', context)