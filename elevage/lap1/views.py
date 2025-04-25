from django.shortcuts import render, redirect, get_object_or_404
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
   

def menu(request):
    return render(request, 'lap1/menu.html')

def gameover(request):
    return render (request, 'lap1/gameover.html')

def delete_elevage(request, elevage_id):
    elevage = get_object_or_404(Elevage, id=elevage_id)
    elevage.delete()
    return redirect('liste')

def actions(request, elevage_id):
    try:
        elevage = Elevage.objects.get(id=elevage_id)
    except ObjectDoesNotExist:
        return render(request, 'lap1/error.html', {'message': "Élevage introuvable."})
    
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            lapins_males_a_vendre    = int(request.POST.get('sale_lapins', 0))
            lapins_femelles_a_vendre = int(request.POST.get('sale_lapins2',  0))
            lapins_males_a_acheter   = int(request.POST.get('achat_males',   0))
            lapins_femelles_a_acheter= int(request.POST.get('achat_femelles',0))
            nourriture_a_acheter     = int(request.POST.get('achat_nourriture', 0))
            nb_gestation             = int(request.POST.get('gestation', 0))

            price_nourriture = Regle.objects.first().price_food
            total_courses    = nourriture_a_acheter * price_nourriture

        
            if lapins_males_a_vendre > elevage.Nombre_de_lapins_males:
                form.add_error('sale_lapins', "Pas assez de lapins mâles.")
            elif lapins_femelles_a_vendre > elevage.Nombre_de_lapins_femelles:
                form.add_error('sale_lapins2', "Pas assez de lapins femelles.")
            elif total_courses > elevage.Argent_initial:
                form.add_error('achat_nourriture',
                    f"Pas assez d'argent : il te faut {total_courses} € pour {nourriture_a_acheter} g.")
            else:

                # vendre lapins
                if lapins_males_a_vendre > 0:
                    males = list(Individu.objects
                        .filter(elevage=elevage, sexe='M', etat='P', age__gte=6)
                        .order_by('?'))
                    for lapin in males[:lapins_males_a_vendre]:
                        lapin.delete()

                if lapins_femelles_a_vendre > 0:
                    femelles = list(Individu.objects
                        .filter(elevage=elevage, sexe='F', etat='P', age__gte=6)
                        .order_by('?'))
                    for lapin in femelles[:lapins_femelles_a_vendre]:
                        lapin.delete()

                # — enceintes, chosiir aléatoire
                femelles_libres = list(Individu.objects
                    .filter(elevage=elevage, sexe='F', etat='P', age__gte=6)
                    .order_by('?'))
                nb_gest = min(nb_gestation, len(femelles_libres))
                for femelle in femelles_libres[:nb_gest]:
                    femelle.etat = 'G'
                    femelle.mois_debut_gestation = elevage.mois
                    femelle.save()
                elevage.Nombre_de_femelles_en_gestation += nb_gest

                # — accouchement
                accoucheuses = []
                for femelle in Individu.objects.filter(elevage=elevage, sexe='F', etat='G'):
                    if elevage.mois - femelle.mois_debut_gestation >= 6:
                        for _ in range(random.randint(1,4)):
                            Individu.objects.create(
                                elevage=elevage, sexe=random.choice(['M','F']),
                                age=0, etat='P'
                            )
                        femelle.etat = 'P'
                        femelle.mois_debut_gestation = None
                        femelle.save()
                        accoucheuses.append(femelle)

                # — pas assez de cages
                vivants = list(Individu.objects.filter(elevage=elevage, etat__in=['P','G']))
                surplus = len(vivants) - elevage.Nombre_de_cages * 6
                if surplus > 0:
                    random.shuffle(vivants)
                    for ind in vivants[:surplus]:
                        ind.etat = 'M'
                        ind.save()


                adultes = Individu.objects.filter(elevage=elevage, age__gte=3)
                ados    = Individu.objects.filter(elevage=elevage, age=2)
                conso_ado = Regle.objects.first().conso_nourriture_2mois
                conso_adulte = Regle.objects.first().conso_nourriture_3mois
                total_conso = adultes.count() * conso_adulte
                total_conso += ados.count() * conso_ado

                # — maj chaque mois
                # nourriture
                elevage.Argent_initial       -= total_courses
                elevage.Nourriture_disponible += nourriture_a_acheter - total_conso
                # recettes ventes lapins
                prix_vente = Regle.objects.first().price_sale_lapin
                recettes = (lapins_males_a_vendre + lapins_femelles_a_vendre) * prix_vente
                achats   = (lapins_males_a_acheter + lapins_femelles_a_acheter) * prix_vente
                elevage.Argent_initial += recettes - achats
                # stock 
                elevage.Nombre_de_lapins_males   += lapins_males_a_acheter - lapins_males_a_vendre
                elevage.Nombre_de_lapins_femelles+= lapins_femelles_a_acheter - lapins_femelles_a_vendre
                # femelles enceijtes
                elevage.Nombre_de_femelles_en_gestation = max(
                    0,
                    elevage.Nombre_de_femelles_en_gestation - len(accoucheuses)
                )

                # — PASSAGE DU MOIS
                for individu in Individu.objects.filter(elevage=elevage):
                    individu.age += 1
                    if individu.age > 48:
                        individu.delete()
                    else:
                        individu.save()
                elevage.mois += 1
                elevage.save()

                if elevage.Nombre_de_lapins_femelles + elevage.Nombre_de_lapins_males <=0: 
                    return render(request, 'lap1/gameover.html')

                return redirect('elevage', elevage_id=elevage.id)
        

        return render(request, 'lap1/elevage.html', {'form': form, 'elevage': elevage})
    
    form = ActionForm()
    return render(request, 'lap1/elevage.html', {'form': form, 'elevage': elevage})
