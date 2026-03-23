from django.shortcuts import render

# Create your views here.
def student_list(request):
    return render(request, 'students/students.html')

def add_student(request):
    return render(request, 'students/add-student.html')