from django.shortcuts import render, redirect, get_object_or_404
from .models import Exam, Result
from student.models import Student

# list exam
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exam/exam_list.html', {'exams': exams})



# add exam
def add_exam(request):
    if request.method == 'POST':
        Exam.objects.create(
            title=request.POST.get('title'),
            subject=request.POST.get('subject'),
            date=request.POST.get('date'),
            duration=request.POST.get('duration'),
            room=request.POST.get('room'),
            coefficient=request.POST.get('coefficient'),
        )
        return redirect('exam_list')

    return render(request, 'exam/add_exam.html')


# delete
def delete_exam(request, id):
    exam = get_object_or_404(Exam, id=id)
    exam.delete()
    return redirect('exam_list')
