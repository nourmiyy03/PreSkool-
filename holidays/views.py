from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import Holiday
import calendar
from datetime import datetime, timedelta

# Vérification admin
def is_admin(user):
    return user.is_admin or user.is_superuser


@login_required
def holiday_list(request):
    """Liste de tous les jours fériés"""
    holidays = Holiday.objects.all()
    return render(request, 'holidays/holiday_list.html', {'holidays': holidays})


@login_required
def holiday_calendar(request):
    """Vue calendrier des jours fériés"""
    # Récupérer l'année et le mois depuis l'URL ou utiliser la date actuelle
    year = request.GET.get('year', datetime.now().year)
    month = request.GET.get('month', datetime.now().month)
    
    try:
        year = int(year)
        month = int(month)
    except:
        year = datetime.now().year
        month = datetime.now().month
    
    # Récupérer les jours fériés du mois
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    holidays = Holiday.objects.filter(
        start_date__lt=end_date,
        end_date__gte=start_date
    )
    
    # Créer le calendrier
    cal = calendar.monthcalendar(year, month)
    
    # Préparer la navigation
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    context = {
        'calendar': cal,
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'holidays': holidays,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    }
    
    return render(request, 'holidays/holiday_calendar.html', context)


@login_required
@user_passes_test(is_admin)
def add_holiday(request):
    """Ajouter un jour férié (admin uniquement)"""
    if request.method == 'POST':
        name = request.POST.get('name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')
        holiday_type = request.POST.get('type')
        
        Holiday.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date,
            description=description,
            type=holiday_type
        )
        
        messages.success(request, 'Jour férié ajouté avec succès!')
        return redirect('holiday_list')
    
    return render(request, 'holidays/add_holiday.html')


@login_required
@user_passes_test(is_admin)
def edit_holiday(request, holiday_id):
    """Modifier un jour férié"""
    holiday = get_object_or_404(Holiday, id=holiday_id)
    
    if request.method == 'POST':
        holiday.name = request.POST.get('name')
        holiday.start_date = request.POST.get('start_date')
        holiday.end_date = request.POST.get('end_date')
        holiday.description = request.POST.get('description')
        holiday.type = request.POST.get('type')
        holiday.save()
        
        messages.success(request, 'Jour férié modifié avec succès!')
        return redirect('holiday_list')
    
    return render(request, 'holidays/edit_holiday.html', {'holiday': holiday})


@login_required
@user_passes_test(is_admin)
def delete_holiday(request, holiday_id):
    """Supprimer un jour férié"""
    holiday = get_object_or_404(Holiday, id=holiday_id)
    holiday.delete()
    messages.success(request, 'Jour férié supprimé avec succès!')
    return redirect('holiday_list')
