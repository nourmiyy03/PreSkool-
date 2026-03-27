from django.db import models
from subjects.models import Subject
from teachers.models import Teacher
from student.models import Student


class TimeTable(models.Model):
    """Modèle pour l'emploi du temps"""
    
    DAYS_OF_WEEK = [
        ('monday', 'Lundi'),
        ('tuesday', 'Mardi'),
        ('wednesday', 'Mercredi'),
        ('thursday', 'Jeudi'),
        ('friday', 'Vendredi'),
        ('saturday', 'Samedi'),
    ]
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Matière")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Enseignant")
    student_class = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Classe", related_name='timetable_entries')
    day = models.CharField(max_length=20, choices=DAYS_OF_WEEK, verbose_name="Jour")
    start_time = models.TimeField(verbose_name="Heure de début")
    end_time = models.TimeField(verbose_name="Heure de fin")
    room = models.CharField(max_length=100, verbose_name="Salle")
    
    def __str__(self):
        return f"{self.subject.name} - {self.student_class.student_class} - {self.get_day_display()} ({self.start_time} - {self.end_time})"
    
    class Meta:
        ordering = ['day', 'start_time']
        verbose_name = "Emploi du temps"
        verbose_name_plural = "Emplois du temps"