import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from home_auth.models import CustomUser
from student.models import Student, Parent

# 1. Supprimer tous les anciens comptes (attention!)
CustomUser.objects.all().delete()
Student.objects.all().delete()
Parent.objects.all().delete()

# 2. Créer un parent
parent = Parent.objects.create(
    father_name="Parent Name",
    father_mobile="0612345678",
    father_email="parent@email.com",
    mother_name="Parent Name",
    mother_mobile="0612345678",
    mother_email="parent@email.com",
    present_address="Address",
    permanent_address="Address"
)

# 3. Créer l'utilisateur étudiant
user = CustomUser.objects.create_user(
    username="wafae@school.com",
    email="wafae@school.com",
    password="wafae123",
    first_name="Wafae",
    last_name="Benali"
)
user.is_student = True
user.save()

# 4. Créer l'étudiant
student = Student.objects.create(
    first_name="Wafae",
    last_name="Benali",
    student_id="STU001",
    gender="Female",
    date_of_birth="2000-01-01",
    student_class="6ème A",
    joining_date="2026-01-01",
    mobile_number="0612345678",
    admission_number="ADM001",
    section="A",
    parent=parent,
    user=user
)

# 5. Créer un super-utilisateur
if not CustomUser.objects.filter(username="admin@school.com").exists():
    admin = CustomUser.objects.create_superuser(
        username="admin@school.com",
        email="admin@school.com",
        password="admin123"
    )
    admin.is_admin = True
    admin.save()

print("=" * 50)
print("✅ COMPTES CRÉÉS AVEC SUCCÈS !")
print("=" * 50)
print("👑 Admin     : admin@school.com / admin123")
print("👨‍🎓 Student   : wafae@school.com / wafae123")
print("=" * 50)