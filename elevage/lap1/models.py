from django.db import models

# Create your models here.
from django.db import models

class Elevage(models.Model):
    Nom_de_mon_elevage = models.CharField(max_length=200)
    Nombre_de_lapins_males = models.IntegerField()
    Nombre_de_lapins_femelles = models.IntegerField()
    Quantité_de_nourriture_initiale = models.FloatField()
    Nombre_de_cages = models.IntegerField()
    Argent_initial = models.FloatField()

    def __str__(self):
        return self.Nom_de_mon_élevage
    
class Individu(models.Model):
    sexe_choix= [
        ('M', 'Mâle'),
        ('F', 'Femelle'),
    ]
    etat_choix = [
        ('P', 'Présent'),
        ('V', 'Vendu'),
        ('M', 'Mort'),
        ('G', 'Gravide'),
    ]
    elevage = models.ForeignKey(Elevage, on_delete=models.CASCADE)
    sexe = models.CharField(max_length=1, choices=sexe_choix)
    age = models.IntegerField()
    etat = models.CharField(max_length=1, choices=etat_choix)

    def __str__(self):
        return self.sexe + " - " + str(self.age) + " mois"
    
class Regle(models.Model):
    price_food = models.FloatField()
    price_cage = models.FloatField()
    price_sale_lapin = models.FloatField()
    conso_nourriture_1mois = models.FloatField()
    conso_nourriture_2mois = models.FloatField()
    conso_nourriture_3mois = models.FloatField()
    nb_max_portee = models.IntegerField()
    nb_max_cage = models.IntegerField()
    age_min_gravide = models.IntegerField()
    age_max_gravide = models.IntegerField()
    duree_gestation = models.IntegerField()

    def __str__(self):
        return "Règles du jeu"