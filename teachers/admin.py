from django.contrib import admin
from .models import Teacher

# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'specialization', 'department', 'hire_date')
    list_filter = ('specialization', 'department', 'hire_date')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'specialization')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone', 'address', 'photo')
        }),
        ('Professional Information', {
            'fields': ('hire_date', 'specialization', 'department')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )