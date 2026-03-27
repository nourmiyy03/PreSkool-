from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import TimeTable
from student.models import Student
from teachers.models import Teacher
from subjects.models import Subject


def is_admin_or_teacher(user):
    return user.is_authenticated and (user.is_admin or user.is_teacher)


@login_required
def timetable_by_class(request, class_id=None):
    """Afficher l'emploi du temps par classe"""
    # Récupérer toutes les classes distinctes
    classes = Student.objects.values_list('student_class', flat=True).distinct()
    
    if class_id:
        selected_class = get_object_or_404(Student, id=class_id)
        timetable = TimeTable.objects.filter(
            student_class=selected_class
        ).select_related('subject', 'teacher', 'student_class')
    else:
        selected_class = None
        timetable = TimeTable.objects.all().select_related('subject', 'teacher', 'student_class')
    
    context = {
        'classes': classes,
        'selected_class': selected_class,
        'timetable': timetable,
    }
    
    return render(request, 'timetable/timetable_by_class.html', context)


@login_required
def timetable_by_teacher(request, teacher_id=None):
    """Afficher l'emploi du temps par enseignant"""
    teachers = Teacher.objects.all()
    
    if teacher_id:
        selected_teacher = get_object_or_404(Teacher, id=teacher_id)
        timetable = TimeTable.objects.filter(
            teacher=selected_teacher
        ).select_related('subject', 'student_class')
    else:
        selected_teacher = None
        timetable = TimeTable.objects.all().select_related('subject', 'teacher', 'student_class')
    
    context = {
        'teachers': teachers,
        'selected_teacher': selected_teacher,
        'timetable': timetable,
    }
    
    return render(request, 'timetable/timetable_by_teacher.html', context)


@login_required
@user_passes_test(is_admin_or_teacher)
def add_timetable(request):
    """Ajouter un cours dans l'emploi du temps (Admin et Teacher)"""
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()
    classes = Student.objects.all()
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher')
        student_class_id = request.POST.get('student_class')
        day = request.POST.get('day')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        room = request.POST.get('room')
        
        # Vérifier que tous les champs sont remplis
        if subject_id and teacher_id and student_class_id and day and start_time and end_time and room:
            TimeTable.objects.create(
                subject_id=subject_id,
                teacher_id=teacher_id,
                student_class_id=student_class_id,
                day=day,
                start_time=start_time,
                end_time=end_time,
                room=room,
            )
            messages.success(request, 'Cours ajouté avec succès!')
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')
        
        return redirect('timetable_by_class')
    
    context = {
        'subjects': subjects,
        'teachers': teachers,
        'classes': classes,
        'days': TimeTable.DAYS_OF_WEEK,
    }
    
    return render(request, 'timetable/add_timetable.html', context)


@login_required
@user_passes_test(is_admin_or_teacher)
def edit_timetable(request, timetable_id):
    """Modifier un cours (Admin et Teacher)"""
    timetable = get_object_or_404(TimeTable, id=timetable_id)
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()
    classes = Student.objects.all()
    
    if request.method == 'POST':
        timetable.subject_id = request.POST.get('subject')
        timetable.teacher_id = request.POST.get('teacher')
        timetable.student_class_id = request.POST.get('student_class')
        timetable.day = request.POST.get('day')
        timetable.start_time = request.POST.get('start_time')
        timetable.end_time = request.POST.get('end_time')
        timetable.room = request.POST.get('room')
        timetable.save()
        
        messages.success(request, 'Cours modifié avec succès!')
        return redirect('timetable_by_class')
    
    context = {
        'timetable': timetable,
        'subjects': subjects,
        'teachers': teachers,
        'classes': classes,
        'days': TimeTable.DAYS_OF_WEEK,
    }
    
    return render(request, 'timetable/edit_timetable.html', context)


@login_required
@user_passes_test(is_admin_or_teacher)
def delete_timetable(request, timetable_id):
    """Supprimer un cours (Admin et Teacher)"""
    timetable = get_object_or_404(TimeTable, id=timetable_id)
    timetable.delete()
    messages.success(request, 'Cours supprimé avec succès!')
    return redirect('timetable_by_class')