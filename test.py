#!/usr/bin/env python
"""
Test script for PreSkool School Management System
This script creates test data for all models in the application.
Run with: python test.py
"""

import os
import django
import random
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

# Import models
from django.contrib.auth import get_user_model
from home_auth.models import CustomUser
from student.models import Student, Parent
from teachers.models import Teacher
from departments.models import Department
from subjects.models import Subject

User = get_user_model()

# Test data
FIRST_NAMES = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emma', 'James', 'Lisa', 'Robert', 'Maria']
LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
SPECIALIZATIONS = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English', 'History', 'Computer Science', 'Physical Education']
SUBJECT_NAMES = [
    ('MATH101', 'Mathematics'), ('PHY101', 'Physics'), ('CHM101', 'Chemistry'),
    ('BIO101', 'Biology'), ('ENG101', 'English'), ('HIS101', 'History'),
    ('CS101', 'Computer Science'), ('PE101', 'Physical Education')
]
DEPARTMENT_NAMES = [
    'Science Department', 'Mathematics Department', 'Languages Department',
    'Humanities Department', 'Computer Science Department', 'Physical Education Department'
]

def create_superuser():
    """Create admin superuser if not exists"""
    if not User.objects.filter(username='admin@preskool.com').exists():
        admin = User.objects.create_superuser(
            username='admin@preskool.com',
            email='admin@preskool.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            is_admin=True,
            is_authorized=True
        )
        print('✓ Admin user created (admin@preskool.com / admin123)')
        return admin
    else:
        admin = User.objects.get(username='admin@preskool.com')
        print('✓ Admin user already exists')
        return admin

def create_test_users():
    """Create test users for teachers and students"""
    users_created = []
    
    # Create 5 teacher users
    for i in range(5):
        username = f'teacher{i+1}@preskool.com'
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=username,
                password='teacher123',
                first_name=FIRST_NAMES[i % len(FIRST_NAMES)],
                last_name=LAST_NAMES[i % len(LAST_NAMES)],
                is_teacher=True,
                is_authorized=True
            )
            users_created.append(user)
            print(f'✓ Teacher user created: {user.first_name} {user.last_name} ({username})')
    
    # Create 10 student users
    for i in range(10):
        username = f'student{i+1}@preskool.com'
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=username,
                password='student123',
                first_name=FIRST_NAMES[i % len(FIRST_NAMES)],
                last_name=LAST_NAMES[i % len(LAST_NAMES)],
                is_student=True,
                is_authorized=True
            )
            users_created.append(user)
            print(f'✓ Student user created: {user.first_name} {user.last_name} ({username})')
    
    return users_created

def create_departments():
    """Create departments"""
    departments = []
    for dept_name in DEPARTMENT_NAMES:
        dept, created = Department.objects.get_or_create(
            name=dept_name,
            defaults={'description': f'Department of {dept_name}'}
        )
        departments.append(dept)
        if created:
            print(f'✓ Department created: {dept.name}')
        else:
            print(f'✓ Department already exists: {dept.name}')
    return departments

def create_teachers(departments):
    """Create teachers linked to users and departments"""
    teachers = []
    teacher_users = User.objects.filter(is_teacher=True)
    
    for i, user in enumerate(teacher_users):
        teacher, created = Teacher.objects.get_or_create(
            user=user,  # Utiliser user comme clé unique
            defaults={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': f'06{random.randint(10000000, 99999999)}',
                'address': f'{random.randint(1, 100)} Main Street, City',
                'hire_date': date(2020, random.randint(1, 12), random.randint(1, 28)),
                'specialization': random.choice(SPECIALIZATIONS),
                'department': random.choice(departments) if departments else None
            }
        )
        teachers.append(teacher)
        if created:
            print(f'✓ Teacher created: {teacher.first_name} {teacher.last_name} - {teacher.specialization}')
        else:
            print(f'✓ Teacher already exists: {teacher.first_name} {teacher.last_name}')
    
    return teachers

def create_parents():
    """Create parents for students - one parent per student"""
    parents = []
    student_count = User.objects.filter(is_student=True).count()
    
    print(f"Creating {student_count} parents...")
    
    for i in range(student_count):
        parent, created = Parent.objects.get_or_create(
            father_name=f'Father {i+1}',
            mother_name=f'Mother {i+1}',
            defaults={
                'father_occupation': random.choice(['Engineer', 'Doctor', 'Teacher', 'Businessman', 'Architect']),
                'father_mobile': f'06{random.randint(10000000, 99999999)}',
                'father_email': f'father{i+1}@example.com',
                'mother_occupation': random.choice(['Doctor', 'Teacher', 'Nurse', 'Lawyer', 'Accountant']),
                'mother_mobile': f'06{random.randint(10000000, 99999999)}',
                'mother_email': f'mother{i+1}@example.com',
                'present_address': f'{random.randint(1, 200)} Present Street, City',
                'permanent_address': f'{random.randint(1, 200)} Permanent Street, City'
            }
        )
        parents.append(parent)
        if created:
            print(f'✓ Parent created: {parent.father_name} & {parent.mother_name}')
    
    return parents

def create_students(parents):
    """Create students linked to users and parents - one parent per student"""
    students = []
    student_users = User.objects.filter(is_student=True)
    classes = ['1st Grade', '2nd Grade', '3rd Grade', '4th Grade', '5th Grade']
    sections = ['A', 'B', 'C']
    
    for i, user in enumerate(student_users):
        # Each student gets a unique parent
        if i >= len(parents):
            print(f"⚠ Not enough parents for student {user.email}")
            break
        
        parent = parents[i]
        
        student, created = Student.objects.get_or_create(
            user=user,
            defaults={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'student_id': f'STU{1000 + i:04d}',
                'gender': random.choice(['Male', 'Female']),
                'date_of_birth': date(2015, random.randint(1, 12), random.randint(1, 28)),
                'student_class': random.choice(classes),
                'joining_date': date(2023, random.randint(8, 9), random.randint(1, 15)),
                'mobile_number': f'06{random.randint(10000000, 99999999)}',
                'admission_number': f'ADM{2000 + i:04d}',
                'section': random.choice(sections),
                'parent': parent
            }
        )
        students.append(student)
        if created:
            print(f'✓ Student created: {student.first_name} {student.last_name} (ID: {student.student_id})')
        else:
            print(f'✓ Student already exists: {student.first_name} {student.last_name}')
    
    return students


def create_subjects(departments, teachers):
    """Create subjects linked to departments and teachers"""
    subjects = []
    
    for code, name in SUBJECT_NAMES:
        subject, created = Subject.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'coefficient': random.choice([1.0, 1.5, 2.0, 2.5, 3.0]),
                'department': random.choice(departments) if departments else None,
                'teacher': random.choice(teachers) if teachers else None,
                'description': f'This is the {name} course, covering fundamental concepts and advanced topics.'
            }
        )
        subjects.append(subject)
        if created:
            print(f'✓ Subject created: {subject.name} ({subject.code})')
        else:
            print(f'✓ Subject already exists: {subject.name}')
    
    return subjects

def assign_department_heads(departments, teachers):
    """Assign head of department for each department"""
    for i, dept in enumerate(departments):
        if i < len(teachers):
            dept.head = teachers[i]
            dept.save()
            print(f'✓ Department head assigned: {dept.name} -> {dept.head.first_name} {dept.head.last_name}')

def print_summary():
    """Print summary of all created data"""
    print("\n" + "="*50)
    print("DATABASE SUMMARY")
    print("="*50)
    
    print(f"\nUsers:")
    print(f"  - Admin: {User.objects.filter(is_admin=True).count()}")
    print(f"  - Teachers: {User.objects.filter(is_teacher=True).count()}")
    print(f"  - Students: {User.objects.filter(is_student=True).count()}")
    print(f"  - Total: {User.objects.count()}")
    
    print(f"\nTeachers: {Teacher.objects.count()}")
    print(f"Students: {Student.objects.count()}")
    print(f"Parents: {Parent.objects.count()}")
    print(f"Departments: {Department.objects.count()}")
    print(f"Subjects: {Subject.objects.count()}")
    
    print("\n" + "="*50)
    print("LOGIN CREDENTIALS")
    print("="*50)
    print("\nAdmin Login:")
    print("  Email: admin@preskool.com")
    print("  Password: admin123")
    
    print("\nTeacher Login (any):")
    print("  Email: teacher1@preskool.com, teacher2@preskool.com, ...")
    print("  Password: teacher123")
    
    print("\nStudent Login (any):")
    print("  Email: student1@preskool.com, student2@preskool.com, ...")
    print("  Password: student123")
    print("\n" + "="*50)

def run_tests():
    """Main function to run all tests"""
    print("\n" + "="*50)
    print("PRE-SKOOL TEST DATA GENERATOR")
    print("="*50 + "\n")
    
    print("Creating test data...\n")
    
    # Create data in correct order
    create_superuser()
    create_test_users()
    departments = create_departments()
    teachers = create_teachers(departments)
    assign_department_heads(departments, teachers)
    parents = create_parents()
    students = create_students(parents)
    subjects = create_subjects(departments, teachers)
    
    # Print summary
    print_summary()
    
    print("\n✓ Test data generation completed successfully!")
    print("\nYou can now run the server:")
    print("  python manage.py runserver")
    print("\nAnd login with the credentials above.\n")

if __name__ == '__main__':
    run_tests()