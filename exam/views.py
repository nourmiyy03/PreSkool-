from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Exam, Result
from student.models import Student
from subjects.models import Subject
from teachers.models import Teacher  


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
    """Liste des examens - filtre selon le rôle"""
    user = request.user
    
    if user.is_admin or user.is_superuser:
        # Admin voit tous les examens
        exams = Exam.objects.all()
    elif user.is_teacher:
        # Enseignant voit uniquement les examens de ses matières
        try:
            teacher = Teacher.objects.get(user=user)
            exams = Exam.objects.filter(subject__teacher=teacher)
        except Teacher.DoesNotExist:
            exams = Exam.objects.none()
    else:
        # Étudiant ne voit pas les examens (redirection)
        return redirect('my_results')
    
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
    """Saisie des notes - enseignant ne peut saisir que pour ses matières"""
    exam = get_object_or_404(Exam, id=exam_id)
    user = request.user
    
    # Vérifier que l'enseignant a le droit de modifier cet examen
    if user.is_teacher:
        try:
            teacher = Teacher.objects.get(user=user)
            if exam.subject.teacher != teacher:
                messages.error(request, "Vous n'êtes pas autorisé à saisir les notes pour cet examen.")
                return redirect('exam_list')
        except Teacher.DoesNotExist:
            messages.error(request, "Profil enseignant non trouvé.")
            return redirect('exam_list')
    
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