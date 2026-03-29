from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Exam, Result
from student.models import Student
from subjects.models import Subject


def is_admin(user):
    return user.is_authenticated and (user.is_admin or user.is_superuser)

def is_teacher_or_admin(user):
    return user.is_authenticated and (user.is_teacher or user.is_admin)

def is_teacher_only(user):
    return user.is_authenticated and user.is_teacher and not user.is_admin

def is_student(user):
    return user.is_authenticated and user.is_student


@login_required
def exam_list(request):
    """Liste des examens - accessible à tous les connectés"""
    exams = Exam.objects.all()
    return render(request, 'exam/exam_list.html', {'exams': exams})


@login_required
def add_exam(request):
    """Ajouter un examen - uniquement admin"""
    if not is_admin(request.user):
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('exam_list')
    
    subjects = Subject.objects.all()
    
    if request.method == 'POST':
        Exam.objects.create(
            title=request.POST.get('title'),
            subject_id=request.POST.get('subject'),
            date=request.POST.get('date'),
            duration=request.POST.get('duration'),
            room=request.POST.get('room'),
            coefficient=request.POST.get('coefficient'),
            description=request.POST.get('description'),
        )
        messages.success(request, 'Examen ajouté avec succès!')
        return redirect('exam_list')
    
    return render(request, 'exam/add_exam.html', {'subjects': subjects})


@login_required
def edit_exam(request, exam_id):
    """Modifier un examen - uniquement admin"""
    if not is_admin(request.user):
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('exam_list')
    
    exam = get_object_or_404(Exam, id=exam_id)
    subjects = Subject.objects.all()
    
    if request.method == 'POST':
        exam.title = request.POST.get('title')
        exam.subject_id = request.POST.get('subject')
        exam.date = request.POST.get('date')
        exam.duration = request.POST.get('duration')
        exam.room = request.POST.get('room')
        exam.coefficient = request.POST.get('coefficient')
        exam.description = request.POST.get('description')
        exam.save()
        messages.success(request, 'Examen modifié avec succès!')
        return redirect('exam_list')
    
    return render(request, 'exam/edit_exam.html', {'exam': exam, 'subjects': subjects})


@login_required
def delete_exam(request, exam_id):
    """Supprimer un examen - uniquement admin"""
    if not is_admin(request.user):
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('exam_list')
    
    exam = get_object_or_404(Exam, id=exam_id)
    exam.delete()
    messages.success(request, 'Examen supprimé avec succès!')
    return redirect('exam_list')


@login_required
def add_result(request, exam_id):
    """Saisie des notes - enseignant uniquement (admin peut aussi)"""
    if not is_teacher_or_admin(request.user):
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('exam_list')
    
    exam = get_object_or_404(Exam, id=exam_id)
    students = Student.objects.all()
    
    if request.method == 'POST':
        for student in students:
            score = request.POST.get(f'score_{student.id}')
            comment = request.POST.get(f'comment_{student.id}')
            if score:
                Result.objects.update_or_create(
                    student=student,
                    exam=exam,
                    defaults={'score': score, 'comment': comment}
                )
        messages.success(request, 'Notes enregistrées avec succès!')
        return redirect('exam_list')
    
    results = {r.student_id: r for r in Result.objects.filter(exam=exam)}
    return render(request, 'exam/add_result.html', {
        'exam': exam,
        'students': students,
        'results': results,
    })


@login_required
def my_results(request):
    """Consulter mes notes - étudiant uniquement"""
    if not is_student(request.user):
        messages.error(request, "Vous n'avez pas accès à cette page.")
        return redirect('exam_list')
    
    try:
        student = Student.objects.get(user=request.user)
        results = Result.objects.filter(student=student).select_related('exam')
    except Student.DoesNotExist:
        results = []
    
    return render(request, 'exam/my_results.html', {'results': results})