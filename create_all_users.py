import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from home_auth.models import CustomUser
from student.models import Student, Parent
from teachers.models import Teacher
from departments.models import Department


# 1. Supprimer tous les anciens comptes (attention!)
print("🗑️ Suppression des anciennes données...")
CustomUser.objects.all().delete()
Student.objects.all().delete()
Parent.objects.all().delete()
Teacher.objects.all().delete()
Department.objects.all().delete()


# 2. Créer un département
print("📁 Création du département...")
department = Department.objects.create(
    name="Informatique",
    description="Département des sciences informatiques",
    # created_at enlevé car n'existe pas dans le modèle
)


# 3. Créer un parent
print("👨‍👩‍👧 Création du parent...")
parent = Parent.objects.create(
    father_name="Mohamed Benali",
    father_occupation="Ingénieur",
    father_mobile="0612345678",
    father_email="mohamed.benali@email.com",
    mother_name="Fatima Benali",
    mother_occupation="Enseignante",
    mother_mobile="0612345679",
    mother_email="fatima.benali@email.com",
    present_address="123 Rue de Rabat, Maroc",
    permanent_address="123 Rue de Rabat, Maroc"
)


# 4. Créer l'utilisateur étudiant
print("👨‍🎓 Création de l'étudiant...")
user_student = CustomUser.objects.create_user(
    username="wafae@school.com",
    email="wafae@school.com",
    password="wafae123",
    first_name="Wafae",
    last_name="Benali"
)
user_student.is_student = True
user_student.save()

# 5. Créer l'étudiant
student = Student.objects.create(
    first_name="Wafae",
    last_name="Benali",
    student_id="STU001",
    gender="Female",
    date_of_birth="2010-05-15",
    student_class="6ème A",
    joining_date="2026-01-01",
    mobile_number="0612345680",
    admission_number="ADM001",
    section="A",
    parent=parent,
    user=user_student
)


# 6. Créer l'utilisateur enseignant
print("👨‍🏫 Création de l'enseignant...")
user_teacher = CustomUser.objects.create_user(
    username="karim@school.com",
    email="karim@school.com",
    password="teacher123",
    first_name="Karim",
    last_name="Alami"
)
user_teacher.is_teacher = True
user_teacher.save()

# 7. Créer l'enseignant
teacher = Teacher.objects.create(
    user=user_teacher,
    first_name="Karim",
    last_name="Alami",
    email="karim@school.com",
    phone="0612345690",
    address="45 Rue de Casablanca, Maroc",
    specialization="Développement Web",
    department=department,
    hire_date="2024-09-01"
)


# 8. Créer un super-utilisateur (Admin)
print("👑 Création de l'administrateur...")
if not CustomUser.objects.filter(username="admin@school.com").exists():
    admin = CustomUser.objects.create_superuser(
        username="admin@school.com",
        email="admin@school.com",
        password="admin123"
    )
    admin.is_admin = True
    admin.save()


print("=" * 60)
print("✅ COMPTES CRÉÉS AVEC SUCCÈS !")
print("=" * 60)
print("👑 Admin      : admin@school.com / admin123")
print("👨‍🏫 Teacher    : karim@school.com / teacher123")
print("👨‍🎓 Student    : wafae@school.com / wafae123")
print("=" * 60)
print("📋 Informations supplémentaires :")
print(f"   📁 Département: {department.name}")
print(f"   👨‍🏫 Enseignant: {teacher.first_name} {teacher.last_name}")
print(f"   👨‍🎓 Étudiant: {student.first_name} {student.last_name} (ID: {student.student_id})")
print("=" * 60)