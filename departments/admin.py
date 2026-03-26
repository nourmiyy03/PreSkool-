from django.contrib import admin
from .models import Department

# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('name', 'description')
    
    fieldsets = (
        ('Department Information', {
            'fields': ('name', 'description', 'head')
        }),
        ('Metadata', {
            'fields': ('created_date',),
            'classes': ('collapse',)
        }),
    )