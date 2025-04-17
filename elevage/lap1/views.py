from django.shortcuts import render, redirect
from .models import Elevage, Individu, Regle
from .forms import DebutForm, ActionForm
import random


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
            elevage = form.save()  # Sauvegarde de l'élevage

            # Génération des individus
            for _ in range(elevage.Nombre_de_lapins_males):
                Individu.objects.create(
                    elevage=elevage,
                    sexe='M',
                    age=random.randint(1, 36),
                    etat='P'
                )

            for _ in range(elevage.Nombre_de_lapins_femelles):
                Individu.objects.create(
                    elevage=elevage,
                    sexe='F',
                    age=random.randint(1, 36),
                    etat='P'
                )

            return redirect('liste')
        else:
            return render(request, 'lap1/nouveau.html', {'form': form})
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
            lapins_males_a_vendre = request.POST.get('sale_lapins')
            try:
                lapins_males_a_vendre = int(lapins_males_a_vendre)
            except (ValueError, TypeError):
                lapins_males_a_vendre = 0 

            lapins_femelles_a_vendre =request.POST.get('sale_lapins2')
            try:
                lapins_femelles_a_vendre = int(lapins_femelles_a_vendre)
            except (ValueError, TypeError):
                lapins_femelles_a_vendre = 0 
            
            nb_gestation =request.POST.get('gestation')
            try:
                nb_gestation = int(nb_gestation)
            except (ValueError, TypeError):
                nb_gestation = 0 
            


            nourriture_a_acheter = request.POST.get('achat_nourriture')
            try:
                nourriture_a_acheter = int(nourriture_a_acheter)
            except (ValueError, TypeError):
                nourriture_a_acheter = 0 
            
            if lapins_males_a_vendre > elevage.Nombre_de_lapins_males:
                form.add_error('sale_lapins', "Pas assez de lapins.")
            elif lapins_femelles_a_vendre > elevage.Nombre_de_lapins_femelles:
                form.add_error('achat_nourriture', "Pas assez d'argent.")
            elif nourriture_a_acheter > elevage.Argent_initial:
                form.add_error('achat_nourriture', "Pas assez d'argent.")
            else:
                regles = Regle.objects.first()
                price_nourriture = regles.price_food

                total_courses = nourriture_a_acheter * price_nourriture

                elevage.Nombre_de_lapins_males = elevage.Nombre_de_lapins_males - lapins_males_a_vendre
                elevage.Nombre_de_lapins_femelles = elevage.Nombre_de_lapins_femelles - lapins_femelles_a_vendre
                elevage.Argent_initial = elevage.Argent_initial - total_courses
                elevage.Nombre_de_femelles_en_gestation = elevage.Nombre_de_femelles_en_gestation + nb_gestation
                elevage.Nourriture_disponible = elevage.Nourriture_disponible + nourriture_a_acheter
                elevage.save() 
                
                return redirect('elevage', elevage_id=elevage.id)
        else:
            return render(request, 'lap1/actions.html', {'form': form, 'elevage': elevage})
        
    return render(request, 'lap1/actions.html', {'form': form, 'elevage': elevage})

def menu(request):
    return render(request, 'lap1/menu.html')
