from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Parent
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

# Fonctions de vérification des rôles
def is_admin_or_teacher(user):
    """Vérifie si l'utilisateur est admin ou enseignant"""
    return user.is_authenticated and (user.is_admin or user.is_teacher or user.is_superuser)

def is_admin(user):
    """Vérifie si l'utilisateur est admin"""
    return user.is_authenticated and (user.is_admin or user.is_superuser)

def is_student(user):
    """Vérifie si l'utilisateur est étudiant"""
    return user.is_authenticated and user.is_student


@login_required
@user_passes_test(is_admin_or_teacher)
def student_list(request):
    """Liste des étudiants - accessible uniquement aux admins et enseignants"""
    students = Student.objects.all()
    return render(request, 'students/students.html', {'students': students})


@login_required
@user_passes_test(is_admin_or_teacher)
def add_student(request):
    """Ajouter un étudiant - accessible uniquement aux admins et enseignants"""
    if request.method == 'POST':
        # Récupérer les données de l'étudiant
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')
        
        # Récupérer les données du parent
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        
        # Créer le parent
        parent = Parent.objects.create(
            father_name=father_name,
            father_occupation=father_occupation,
            father_mobile=father_mobile,
            father_email=father_email,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            mother_mobile=mother_mobile,
            mother_email=mother_email,
            present_address=present_address,
            permanent_address=permanent_address
        )
        
        # Créer l'étudiant
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            gender=gender,
            date_of_birth=date_of_birth,
            student_class=student_class,
            joining_date=joining_date,
            mobile_number=mobile_number,
            admission_number=admission_number,
            section=section,
            student_image=student_image,
            parent=parent
        )
        
        messages.success(request, 'Student added Successfully')
        return redirect('student_list')
    else:
        return render(request, 'students/add-student.html')


@login_required
@user_passes_test(is_admin_or_teacher)
def edit_student(request, student_id):
    """Modifier un étudiant - accessible uniquement aux admins et enseignants"""
    student = get_object_or_404(Student, student_id=student_id)
    parent = student.parent

    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.student_class = request.POST.get('student_class')
        student.mobile_number = request.POST.get('mobile_number')
        student.section = request.POST.get('section')

        # update parent
        parent.father_name = request.POST.get('father_name')
        parent.mother_name = request.POST.get('mother_name')

        student.save()
        parent.save()

        messages.success(request, 'Student updated successfully')
        return redirect('student_list')

    return render(request, 'students/edit-student.html', {'student': student})


@login_required
def view_student(request, student_id):
    """Voir les détails d'un étudiant - accessible à tous les utilisateurs connectés"""
    student = get_object_or_404(Student, student_id=student_id)
    
    # Si l'utilisateur est un étudiant, il ne peut voir que sa propre fiche
    if request.user.is_student:
        try:
            if student.user != request.user:
                messages.error(request, "Vous ne pouvez voir que votre propre fiche.")
                return redirect('student_dashboard')
        except:
            messages.error(request, "Vous ne pouvez voir que votre propre fiche.")
            return redirect('student_dashboard')
    
    return render(request, 'students/student-details.html', {'student': student})


@login_required
@user_passes_test(is_admin_or_teacher)
def delete_student(request, student_id):
    """Supprimer un étudiant - accessible uniquement aux admins et enseignants"""
    student = get_object_or_404(Student, student_id=student_id)
    student.delete()
    messages.success(request, 'Student deleted successfully')
    return redirect('student_list')