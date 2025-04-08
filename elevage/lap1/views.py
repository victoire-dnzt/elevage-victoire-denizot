from django.shortcuts import render, redirect
from .models import Elevage, Individu, Regle
from .forms import DebutForm, ActionForm

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
    
def calcul_lapins(request, elevage_id):
    elevage = Elevage.objects.get(id=elevage_id)
    total_lapins = elevage.Nombre_de_lapins_femelles + elevage.Nombre_de_lapins_males
    return render(request, 'lap1/elevage.html', {'elevage': elevage, 'total_lapins': total_lapins})
    
def actions(request, elevage_id):
    elevage = Elevage.objects.get(id=elevage_id)
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            lapins_a_vendre ='sale_lapins'
            nourriture_a_acheter ='achat_nourriture'
            
            if lapins_a_vendre > elevage.nombre_lapins:
                form.add_error('sale_lapins', "Pas le droit vendre plus de lapins que vous n'en avez, pardi.")
            elif nourriture_a_acheter > elevage.argent_caisse:
                form.add_error('achat_nourriture', "Pas assez d'argent, désolé.")
            else:
                elevage.nombre_lapins = elevage.nombre_lapins - lapins_a_vendre 
                elevage.quantite_nourriture = elevage.quantite_nourriture+ nourriture_a_acheter  
                elevage.argent_caisse = elevage.argent_caisse + nourriture_a_acheter  
                elevage.save() 
                
                return redirect('elevage', elevage_id=elevage.id) 
        else:
            # Si le formulaire n'est pas valide, on le renvoie avec les erreurs
            return render(request, 'lap1/actions.html', {'form': form, 'elevage': elevage})
    
    else:
        # Affichage du formulaire vide
        form = ActionForm()
    
    return render(request, 'lap1/actions.html', {'form': form, 'elevage': elevage})

def menu(request):
    return render(request, 'lap1/menu.html')