from django.contrib import admin
from .models import Subject

# Register your models here.

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'coefficient', 'department', 'teacher')
    list_filter = ('department', 'coefficient', 'created_at')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Subject Information', {
            'fields': ('name', 'code', 'coefficient', 'description')
        }),
        ('Relationships', {
            'fields': ('department', 'teacher')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )