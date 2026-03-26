from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Teacher
from departments.models import Department

# Create your views here.


def is_admin(user):
    return user.is_authenticated and user.is_admin

@login_required
@user_passes_test(is_admin)
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher-list.html', {'teachers': teachers})

@login_required
@user_passes_test(is_admin)
def teacher_add(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        teacher = Teacher.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            hire_date=request.POST.get('hire_date'),
            specialization=request.POST.get('specialization'),
            photo=request.FILES.get('photo'),
            department_id=request.POST.get('department')
        )
        messages.success(request, 'Teacher added successfully!')
        return redirect('teacher_list')
    return render(request, 'teachers/add-teacher.html', {'departments': departments})

@login_required
@user_passes_test(is_admin)
def teacher_edit(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    departments = Department.objects.all()
    if request.method == 'POST':
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.email = request.POST.get('email')
        teacher.phone = request.POST.get('phone')
        teacher.address = request.POST.get('address')
        teacher.hire_date = request.POST.get('hire_date')
        teacher.specialization = request.POST.get('specialization')
        if request.FILES.get('photo'):
            teacher.photo = request.FILES.get('photo')
        teacher.department_id = request.POST.get('department')
        teacher.save()
        messages.success(request, 'Teacher updated successfully!')
        return redirect('teacher_list')
    return render(request, 'teachers/edit-teacher.html', {'teacher': teacher, 'departments': departments})

@login_required
@user_passes_test(is_admin)
def teacher_delete(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully!')
        return redirect('teacher_list')
    return render(request, 'teachers/delete-teacher.html', {'teacher': teacher})

@login_required
@user_passes_test(is_admin)
def teacher_view(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'teachers/teacher-details.html', {'teacher': teacher})