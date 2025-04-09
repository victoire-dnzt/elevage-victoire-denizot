from django.shortcuts import render, redirect
from .models import Elevage, Individu, Regle
from .forms import DebutForm, ActionForm

from django.core.exceptions import ObjectDoesNotExist


def liste(request):
    elevages = Elevage.objects.all()
    return render(request, 'lap1/liste.html', {'elevages': elevages})

def elevage(request, elevage_id):
    elevage = Elevage.objects.get(id=elevage_id)
    individus = Individu.objects.filter(elevage=elevage)
    return render(request, 'lap1/elevage.html', {'elevage': elevage, 'individus': individus})

def nouveau(request):
    form = DebutForm()
    return render(request, 'lap1/nouveau.html', {'form': form})

def index(request):
    return render(request, 'lap1/index.html')

def regles(request):
    regles = Regle.objects.all()
    return render(request, 'lap1/regles.html', {'regles':regles})

def new_elevage(request):
    if request.method == 'POST':
        form = DebutForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('liste') 
        else:
            return 'Pas valide'
    else:
        form = DebutForm()
        return render(request, 'lap1/nouveau.html', {'form': form})
    
    
def actions(request, elevage_id):
    try:
        elevage = Elevage.objects.get(id=elevage_id)
    except ObjectDoesNotExist:
        return render(request, 'lap1/error.html', {'message': "Élevage introuvable."})

    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            lapins_a_vendre = request.POST.get('sale_lapins')
            try:
                lapins_a_vendre = int(lapins_a_vendre)
            except (ValueError, TypeError):
                lapins_a_vendre = 0 
            nourriture_a_acheter = request.POST.get('achat_nourriture')
            try:
                nourriture_a_acheter = int(nourriture_a_acheter)
            except (ValueError, TypeError):
                nourriture_a_acheter = 0 
            
            if lapins_a_vendre > elevage.Nombre_de_lapins_femelles + elevage.Nombre_de_lapins_males:
                form.add_error('sale_lapins', "Pas assez de lapins.")
            elif nourriture_a_acheter > elevage.Argent_initial:
                form.add_error('achat_nourriture', "Pas assez d'argent.")
            else:
                elevage.Nombre_de_lapins_femelles = elevage.Nombre_de_lapins_femelles - lapins_a_vendre
                elevage.Quantité_de_nourriture_initiale = elevage.Quantité_de_nourriture_initiale+ nourriture_a_acheter  
                elevage.Argent_initial = elevage.Argent_initial + nourriture_a_acheter  
                elevage.save() 
                
                return redirect('elevage', elevage_id=elevage.id)
        else:
            return render(request, 'lap1/actions.html', {'form': form, 'elevage': elevage})
    
    else:
        form = ActionForm()
    
        return render(request, 'lap1/actions.html', {'form': form, 'elevage': elevage})

def menu(request):
    return render(request, 'lap1/menu.html')