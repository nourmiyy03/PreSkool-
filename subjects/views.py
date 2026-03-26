from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Subject
from departments.models import Department
from teachers.models import Teacher

# Create your views here.

def is_admin(user):
    return user.is_authenticated and user.is_admin

@login_required
@user_passes_test(is_admin)
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/subject-list.html', {'subjects': subjects})

@login_required
@user_passes_test(is_admin)
def subject_add(request):
    departments = Department.objects.all()
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        subject = Subject.objects.create(
            name=request.POST.get('name'),
            code=request.POST.get('code'),
            coefficient=request.POST.get('coefficient'),
            department_id=request.POST.get('department'),
            teacher_id=request.POST.get('teacher') or None,
            description=request.POST.get('description')
        )
        messages.success(request, 'Subject added successfully!')
        return redirect('subject_list')
    return render(request, 'subjects/add-subject.html', {'departments': departments, 'teachers': teachers})

@login_required
@user_passes_test(is_admin)
def subject_edit(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    departments = Department.objects.all()
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        subject.name = request.POST.get('name')
        subject.code = request.POST.get('code')
        subject.coefficient = request.POST.get('coefficient')
        subject.department_id = request.POST.get('department')
        subject.teacher_id = request.POST.get('teacher') or None
        subject.description = request.POST.get('description')
        subject.save()
        messages.success(request, 'Subject updated successfully!')
        return redirect('subject_list')
    return render(request, 'subjects/edit-subject.html', {'subject': subject, 'departments': departments, 'teachers': teachers})

@login_required
@user_passes_test(is_admin)
def subject_delete(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
        return redirect('subject_list')
    return render(request, 'subjects/delete-subject.html', {'subject': subject})