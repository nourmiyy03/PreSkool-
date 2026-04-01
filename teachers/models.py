from django.db import models
from django.contrib.auth import get_user_model
from departments.models import Department  
# Create your models here.


User = get_user_model()
class Teacher(models.Model):
    # Infos personnelles
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
                                null=True, 
                                blank=True,
                                 related_name='teacher_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    # Informations professionnelles
    hire_date = models.DateField()
    specialization = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, 
                                   null=True,
                                    blank=True, 
                                   related_name='teachers')
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['last_name', 'first_name']