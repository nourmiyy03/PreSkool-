#!/usr/bin/env python
"""
Test script for PreSkool School Management System
This script creates test data for all models in the application.
Run with: python test.py
"""

import os
import django
import random
from datetime import date

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

# Student data - each student with their own unique parents
STUDENT_DATA = [
    {'first': 'Nyx', 'last': 'Night', 'gender': 'Male', 'class': '3rd Grade', 
     'father': 'Rhys Night', 'mother': 'Feyre Archer', 'father_occ': 'Architect', 'mother_occ': 'Artist'},
    {'first': 'Velaris', 'last': 'Night', 'gender': 'Female', 'class': '1st Grade',
     'father': 'Rhys Night II', 'mother': 'Feyre Archer II', 'father_occ': 'Architect', 'mother_occ': 'Artist'},
    {'first': 'Silas', 'last': 'Nazari', 'gender': 'Male', 'class': '2nd Grade',
     'father': 'Cassian Nazari', 'mother': 'Nesta Archer', 'father_occ': 'Physical Therapist', 'mother_occ': 'Librarian'},
    {'first': 'Elara', 'last': 'Shadow', 'gender': 'Female', 'class': '5th year',
     'father': 'Azriel Shadow', 'mother': 'Gwyneth Rose', 'father_occ': 'Security Consultant', 'mother_occ': 'Teacher'},
    {'first': 'Andarna', 'last': 'Rios', 'gender': 'Female', 'class': '1st Grade',
     'father': 'Xaden Rios', 'mother': 'Violet Sorrengail', 'father_occ': 'Business Owner', 'mother_occ': 'Writer'},
    {'first': 'Tairn', 'last': 'Rios', 'gender': 'Male', 'class': '3rd Grade',
     'father': 'Xaden Rios II', 'mother': 'Violet Sorrengail II', 'father_occ': 'Business Owner', 'mother_occ': 'Writer'},
    {'first': 'Aura', 'last': 'Mairi', 'gender': 'Female', 'class': '2nd Grade',
     'father': 'Liam Mairi', 'mother': 'Sloane Mairi', 'father_occ': 'Engineer', 'mother_occ': 'Nurse'},
    {'first': 'Aria', 'last': 'Moreland', 'gender': 'Female', 'class': '5th year',
     'father': 'James Moreland', 'mother': 'Sarah Lark', 'father_occ': 'Accountant', 'mother_occ': 'Marketing Manager'},
    {'first': 'Caspian', 'last': 'Moreland', 'gender': 'Male', 'class': '1st Grade',
     'father': 'James Moreland II', 'mother': 'Sarah Lark II', 'father_occ': 'Accountant', 'mother_occ': 'Marketing Manager'},
    {'first': 'Amelia', 'last': 'Basset', 'gender': 'Female', 'class': '2nd Grade',
     'father': 'Simon Basset', 'mother': 'Daphne Basset', 'father_occ': 'Lawyer', 'mother_occ': 'Doctor'},
    {'first': 'David', 'last': 'Basset', 'gender': 'Male', 'class': 'Kindergarten',
     'father': 'Simon Basset II', 'mother': 'Daphne Basset II', 'father_occ': 'Lawyer', 'mother_occ': 'Doctor'},
    {'first': 'Edmund', 'last': 'Bridgerton', 'gender': 'Male', 'class': '3rd Grade',
     'father': 'Anthony Bridgerton', 'mother': 'Kate Bridgerton', 'father_occ': 'Banker', 'mother_occ': 'Teacher'},
    {'first': 'Charlotte', 'last': 'Bridgerton', 'gender': 'Female', 'class': '1st Grade',
     'father': 'Anthony Bridgerton II', 'mother': 'Kate Bridgerton II', 'father_occ': 'Banker', 'mother_occ': 'Teacher'},
    {'first': 'Charles', 'last': 'Williams', 'gender': 'Male', 'class': '1st Grade',
     'father': 'Michael Williams', 'mother': 'Emily Williams', 'father_occ': 'Software Developer', 'mother_occ': 'Graphic Designer'},
    {'first': 'Violet', 'last': 'Williams', 'gender': 'Female', 'class': 'Kindergarten',
     'father': 'Michael Williams II', 'mother': 'Emily Williams II', 'father_occ': 'Software Developer', 'mother_occ': 'Graphic Designer'},
    {'first': 'Henry', 'last': 'Goldberg', 'gender': 'Male', 'class': '2nd Grade',
     'father': 'Joseph Goldberg', 'mother': 'Loretta Quinn', 'father_occ': 'Bookstore Owner', 'mother_occ': 'Chef'},
    {'first': 'Lyuba', 'last': 'Miller', 'gender': 'Female', 'class': '3rd Grade',
     'father': 'David Miller', 'mother': 'Anna Miller', 'father_occ': 'Professor', 'mother_occ': 'Journalist'},
]

# Teacher data
TEACHER_DATA = [
    {'first': 'Sarah', 'last': 'Maas', 'specialization': 'English'},
    {'first': 'Rebecca', 'last': 'Yarros', 'specialization': 'History'},
    {'first': 'Ali', 'last': 'Hazelwood', 'specialization': 'Biology'},
    {'first': 'Julia', 'last': 'Quinn', 'specialization': 'English'},
    {'first': 'Caroline', 'last': 'Kepnes', 'specialization': 'Psychology'},
]

def create_superuser():
    """Create admin superuser"""
    if not User.objects.filter(username='admin@preskool.com').exists():
        User.objects.create_superuser(
            username='admin@preskool.com',
            email='admin@preskool.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            is_admin=True,
            is_authorized=True
        )
        print('✓ Admin user created (admin@preskool.com / admin123)')

def create_test_users():
    """Create test users for teachers and students"""
    # Create teacher users
    for teacher in TEACHER_DATA:
        username = f"{teacher['first'].lower()}.{teacher['last'].lower()}@preskool.com"
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                email=username,
                password='teacher123',
                first_name=teacher['first'],
                last_name=teacher['last'],
                is_teacher=True,
                is_authorized=True
            )
            print(f'✓ Teacher user created: {teacher["first"]} {teacher["last"]}')
    
    # Create student users
    for student in STUDENT_DATA:
        username = f"{student['first'].lower()}.{student['last'].lower()}@preskool.com"
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(
                username=username,
                email=username,
                password='student123',
                first_name=student['first'],
                last_name=student['last'],
                is_student=True,
                is_authorized=True
            )
            print(f'✓ Student user created: {student["first"]} {student["last"]}')

def create_departments():
    """Create departments"""
    departments = []
    for dept_name in DEPARTMENT_NAMES:
        dept, _ = Department.objects.get_or_create(
            name=dept_name,
            defaults={'description': f'Department of {dept_name}'}
        )
        departments.append(dept)
        print(f'✓ Department created: {dept.name}')
    return departments

def create_teachers(departments):
    """Create teachers"""
    teachers = []
    teacher_users = User.objects.filter(is_teacher=True)
    
    for user in teacher_users:
        teacher_info = next((t for t in TEACHER_DATA if t['first'] == user.first_name), None)
        specialization = teacher_info['specialization'] if teacher_info else random.choice(SPECIALIZATIONS)
        
        department = None
        for dept in departments:
            if specialization in dept.name or (specialization in ['Physics', 'Chemistry', 'Biology'] and 'Science' in dept.name):
                department = dept
                break
        if not department:
            department = random.choice(departments)
        
        teacher, created = Teacher.objects.get_or_create(
            user=user,
            defaults={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': f'06{random.randint(10000000, 99999999)}',
                'address': f'{random.randint(1, 100)} School Street',
                'hire_date': date(2020, random.randint(1, 12), random.randint(1, 28)),
                'specialization': specialization,
                'department': department
            }
        )
        teachers.append(teacher)
        print(f'✓ Teacher created: {teacher.first_name} {teacher.last_name} - {teacher.specialization}')
    
    return teachers

def create_parents_and_students():
    """Create parents and students (OneToOne relationship)"""
    students = []
    
    for idx, student_data in enumerate(STUDENT_DATA):
        # Create unique parent for this student
        parent = Parent.objects.create(
            father_name=student_data['father'],
            mother_name=student_data['mother'],
            father_occupation=student_data['father_occ'],
            father_mobile=f'06{random.randint(10000000, 99999999)}',
            father_email=f"{student_data['father'].lower().replace(' ', '.')}@example.com",
            mother_occupation=student_data['mother_occ'],
            mother_mobile=f'06{random.randint(10000000, 99999999)}',
            mother_email=f"{student_data['mother'].lower().replace(' ', '.')}@example.com",
            present_address=f'{random.randint(1, 200)} Main Street',
            permanent_address=f'{random.randint(1, 200)} Oak Avenue'
        )
        print(f'✓ Parent created: {parent.father_name} & {parent.mother_name}')
        
        # Get user for this student
        username = f"{student_data['first'].lower()}.{student_data['last'].lower()}@preskool.com"
        user = User.objects.get(username=username)
        
        # Create student with parent (OneToOne)
        student = Student.objects.create(
            user=user,
            first_name=student_data['first'],
            last_name=student_data['last'],
            student_id=f'STU{1000 + idx:04d}',
            gender=student_data['gender'],
            date_of_birth=date(2006, random.randint(1, 12), random.randint(1, 28)),
            student_class=student_data['class'],
            joining_date=date(2023, 9, 1),
            mobile_number=f'06{random.randint(10000000, 99999999)}',
            admission_number=f'ADM{2000 + idx:04d}',
            section=random.choice(['A', 'B', 'C']),
            parent=parent
        )
        students.append(student)
        print(f'✓ Student created: {student.first_name} {student.last_name} (ID: {student.student_id})')
    
    return students

def create_subjects(departments, teachers):
    """Create subjects"""
    subjects = []
    for code, name in SUBJECT_NAMES:
        department = next((d for d in departments if name in d.name), random.choice(departments))
        teacher = next((t for t in teachers if t.specialization == name), random.choice(teachers))
        
        subject, _ = Subject.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'coefficient': random.choice([1.0, 1.5, 2.0, 2.5, 3.0]),
                'department': department,
                'teacher': teacher,
                'description': f'This is the {name} course.'
            }
        )
        subjects.append(subject)
        print(f'✓ Subject created: {subject.name} ({subject.code})')
    return subjects

def assign_department_heads(departments, teachers):
    """Assign department heads"""
    for i, dept in enumerate(departments):
        if i < len(teachers):
            dept.head = teachers[i]
            dept.save()
            print(f'✓ Department head assigned: {dept.name} -> {dept.head.first_name} {dept.head.last_name}')

def print_summary():
    """Print summary"""
    print("\n" + "="*50)
    print("DATABASE SUMMARY")
    print("="*50)
    print(f"\nTeachers: {Teacher.objects.count()}")
    print(f"Students: {Student.objects.count()}")
    print(f"Parents: {Parent.objects.count()}")
    print(f"Departments: {Department.objects.count()}")
    print(f"Subjects: {Subject.objects.count()}")
    
    print("\n" + "="*50)
    print("LOGIN CREDENTIALS")
    print("="*50)
    print("\nAdmin: admin@preskool.com / admin123")
    print("\nTeacher (any): teacher1@preskool.com, etc. / teacher123")
    print("\nStudent (any): nyx.night@preskool.com, etc. / student123")
    print("\n" + "="*50)

def run_tests():
    """Main function"""
    print("\n" + "="*50)
    print("PRE-SKOOL TEST DATA GENERATOR")
    print("="*50 + "\n")
    
    create_superuser()
    create_test_users()
    departments = create_departments()
    teachers = create_teachers(departments)
    assign_department_heads(departments, teachers)
    students = create_parents_and_students()
    subjects = create_subjects(departments, teachers)
    
    print_summary()
    print("\n✓ Test data generation completed successfully!")

if __name__ == '__main__':
    run_tests()