from django.db import models

class Holiday(models.Model):
    """Modèle pour les jours fériés"""
    
    TYPE_CHOICES = [
        ('national', 'National'),
        ('religious', 'Religious'),
        ('special', 'Special'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nom du jour férié")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    description = models.TextField(blank=True, verbose_name="Description")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='national', verbose_name="Type")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"
    
    class Meta:
        ordering = ['start_date']
        verbose_name = "Jour férié"
        verbose_name_plural = "Jours fériés"