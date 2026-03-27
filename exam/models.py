from django.db import models
from student.models import Student
from subjects.models import Subject
from django.utils import timezone


class Exam(models.Model):
    """Modèle pour les examens"""
    title = models.CharField(max_length=200, verbose_name="Titre de l'examen")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Matière")
    date = models.DateField(verbose_name="Date de l'examen")
    duration = models.IntegerField(help_text="Durée en minutes", verbose_name="Durée")
    room = models.CharField(max_length=100, verbose_name="Salle")
    coefficient = models.FloatField(default=1.0, verbose_name="Coefficient")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    
    def __str__(self):
        return f"{self.title} - {self.subject} ({self.date})"
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Examen"
        verbose_name_plural = "Examens"


class Result(models.Model):
    """Modèle pour les résultats d'examens"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Étudiant")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name="Examen")
    score = models.FloatField(default=0.0, verbose_name="Note obtenue")  # ← Ajout default=0.0
    comment = models.TextField(blank=True, verbose_name="Commentaire")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    
    def __str__(self):
        return f"{self.student} - {self.exam} : {self.score}"
    
    class Meta:
        unique_together = ['student', 'exam']
        verbose_name = "Résultat"
        verbose_name_plural = "Résultats"