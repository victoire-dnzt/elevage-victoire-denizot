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

    
def actions(request, elevage_id):
    try:
        elevage = Elevage.objects.get(id=elevage_id)
    except ObjectDoesNotExist:
        return render(request, 'lap1/error.html', {'message': "Élevage introuvable."})
    
    if request.method == 'POST':
        form = ActionForm(request.POST)
        if form.is_valid():
            # recup données, vente achat lapins, nourriture
            lapins_males_a_vendre = int(request.POST.get('sale_lapins', 0))
            lapins_femelles_a_vendre = int(request.POST.get('sale_lapins2', 0))
            lapins_femelles_a_acheter = int(request.POST.get('achat_femelles', 0))
            lapins_males_a_acheter = int(request.POST.get('achat_males', 0))
            nb_gestation = int(request.POST.get('gestation', 0))
            nourriture_a_acheter = int(request.POST.get('achat_nourriture', 0))

            if lapins_males_a_vendre > elevage.Nombre_de_lapins_males:
                form.add_error('sale_lapins', "Pas assez de lapins.")
            elif lapins_femelles_a_vendre > elevage.Nombre_de_lapins_femelles:
                form.add_error('sale_lapins2', "Pas assez de lapins.")
    
                
                #virer les vendus
                if lapins_males_a_vendre > 0:
                    males_eligibles = Individu.objects.filter(elevage=elevage, sexe='M', etat='P', age__gte=6)
                    males_eligibles = list(males_eligibles)
                    if len(males_eligibles) < lapins_males_a_vendre:
                        form.add_error('sale_lapins', "Pas assez de mâles de plus de 3 mois à vendre.")
                    else:
                        for lapin in males_eligibles[:lapins_males_a_vendre]:
                            lapin.delete()

                if lapins_femelles_a_vendre > 0:
                    femelles_eligibles = Individu.objects.filter(elevage=elevage, sexe='F', etat='P', age__gte=6)
                    femelles_eligibles = list(femelles_eligibles)
                    if len(femelles_eligibles) < lapins_femelles_a_vendre:
                        form.add_error('sale_lapins2', "Pas assez de femelles de plus de 3 mois à vendre.")
                    else:
                        for lapin in femelles_eligibles[:lapins_femelles_a_vendre]:
                            lapin.delete()

                # new enceintes
                femelles_libres = Individu.objects.filter(elevage=elevage, sexe='F', etat='P', age__gte=6)
                femelles_libres = list(femelles_libres)
                random.shuffle(femelles_libres)
                nb_gestations = min(nb_gestation, len(femelles_libres))
                femelles_choisies = femelles_libres[:nb_gestations]

                for femelle in femelles_choisies:
                    femelle.etat = 'G'
                    femelle.mois_debut_gestation = elevage.mois
                    femelle.save()

                elevage.Nombre_de_femelles_en_gestation += nb_gestations

                # accoucheemnt des lapins enceintes
                femelles_gravides = Individu.objects.filter(elevage=elevage, sexe='F', etat='G')
                accoucheuses = []

                for femelle in femelles_gravides:
                    duree_gestation_lapin = elevage.mois - femelle.mois_debut_gestation
                    if duree_gestation_lapin >= 6:
                        nb_lapereaux = random.randint(1, 4)
                        for _ in range(nb_lapereaux):
                            sexe = random.choice(['M', 'F'])
                            Individu.objects.create(
                                elevage=elevage,
                                sexe=sexe,
                                age=0,
                                etat='P',
                                mois_debut_gestation=None
                            )
                        femelle.etat = 'P'
                        femelle.mois_debut_gestation = None
                        femelle.save()
                        accoucheuses.append(femelle)

                # pb de cages
                individus_vivants = Individu.objects.filter(elevage=elevage, etat__in=['P', 'G'])
                nb_individus = individus_vivants.count()
                capacite_totale = elevage.Nombre_de_cages * 6

                if nb_individus > capacite_totale:
                    surplus = nb_individus - capacite_totale
                    individus_vivants = list(individus_vivants)
                    random.shuffle(individus_vivants)
                    a_supprimer = individus_vivants[:surplus]
                    for individu in a_supprimer:
                        individu.etat = 'M'
                        individu.save()

                

                regles = Regle.objects.first()
                price_nourriture = regles.price_food
                total_courses = nourriture_a_acheter * price_nourriture

                if total_courses > elevage.Argent_initial:
                    form.add_error('achat_nourriture', "Pas assez d'argent.")
                regles = Regle.objects.first()
                prix_vente_lapin = regles.price_sale_lapin
                total_recettes_ventes = (lapins_femelles_a_vendre + lapins_males_a_vendre) * prix_vente_lapin
                total_depenses_achats = (lapins_femelles_a_acheter + lapins_males_a_acheter) * prix_vente_lapin

                #consommation de nourriture
                
                individus_adultes = Individu.objects.filter(elevage=elevage, age__gte=2)
                nb_individus = individus_adultes.count()
                individus_ados = Individu.objects.filter(elevage=elevage, age=2)
                nb_ados = individus_ados.count()
                regles = Regle.objects.first()
                conso_lap1_adulte = regles.conso_nourriture_3mois
                conso_lap1_ado = regles.conso_nourriture_2mois
                total_conso_lapins = conso_lap1_ado* nb_ados + conso_lap1_adulte * nb_individus


                # lors d'un tour, ce qui change
                elevage.mois += 1
                elevage.Nombre_de_lapins_males = elevage.Nombre_de_lapins_males - lapins_males_a_vendre + lapins_males_a_acheter
                elevage.Nombre_de_lapins_femelles = elevage.Nombre_de_lapins_femelles - lapins_femelles_a_vendre + lapins_femelles_a_acheter
                elevage.Argent_initial = elevage.Argent_initial - total_courses + total_recettes_ventes - total_depenses_achats
                elevage.Nourriture_disponible = elevage.Nourriture_disponible + nourriture_a_acheter - total_conso_lapins
                elevage.Nombre_de_femelles_en_gestation = max(0, elevage.Nombre_de_femelles_en_gestation - len(accoucheuses))

                for individu in Individu.objects.filter(elevage=elevage):
                    individu.age += 1
                    if individu.age > 48:
                        individu.delete()
                    else:
                        individu.save()

                elevage.save()

                if elevage.Nombre_de_lapins_femelles + elevage.Nombre_de_lapins_males <= 0:
                    elevage.delete()
                    return render(request,'lap1/gameover.html')
                elif elevage.Argent_initial <=0:
                    elevage.delete()
                    return render(request, 'lap1/gameover.html')
                elif elevage.Nourriture_disponible<0:
                        elevage.delete()
                        return render(request,'lap1/gameover.html')
                else:
                    return redirect('elevage', elevage_id=elevage.id)
        else:
            return render(request, 'lap1/elevage.html', {'form': form, 'elevage': elevage})
        
    return render(request, 'lap1/elevage.html', {'form': form, 'elevage': elevage})
   

def menu(request):
    return render(request, 'lap1/menu.html')

def gameover(request):
    return render (request, 'lap1/gameover.html')

def delete_elevage(request, elevage_id):
    elevage = get_object_or_404(Elevage, id=elevage_id)
    elevage.delete()
    return redirect('liste')