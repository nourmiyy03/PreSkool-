
from django.db import models
from student.models import Student

class Exam(models.Model):
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    date = models.DateField()
    duration = models.IntegerField()
    room = models.CharField(max_length=50)
    coefficient = models.FloatField()

    def __str__(self):
        return self.title


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    note = models.FloatField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.student} - {self.exam}"
