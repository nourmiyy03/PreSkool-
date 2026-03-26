from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Department
from teachers.models import Teacher

# Create your views here.

def is_admin(user):
    return user.is_authenticated and user.is_admin

@login_required
@user_passes_test(is_admin)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/department-list.html', {'departments': departments})

@login_required
@user_passes_test(is_admin)
def department_add(request):
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        department = Department.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            head_id=request.POST.get('head') or None
        )
        messages.success(request, 'Department added successfully!')
        return redirect('department_list')
    return render(request, 'departments/add-department.html', {'teachers': teachers})

@login_required
@user_passes_test(is_admin)
def department_edit(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.description = request.POST.get('description')
        department.head_id = request.POST.get('head') or None
        department.save()
        messages.success(request, 'Department updated successfully!')
        return redirect('department_list')
    return render(request, 'departments/edit-department.html', {'department': department, 'teachers': teachers})

@login_required
@user_passes_test(is_admin)
def department_delete(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully!')
        return redirect('department_list')
    return render(request, 'departments/delete-department.html', {'department': department})