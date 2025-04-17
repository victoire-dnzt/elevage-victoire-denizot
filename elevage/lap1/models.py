from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Elevage(models.Model):
    Nom_de_mon_elevage = models.CharField(max_length=200)
    Nombre_de_lapins_males = models.IntegerField(validators=[MinValueValidator(0)])
    Nombre_de_lapins_femelles = models.IntegerField(validators=[MinValueValidator(0)])
    Nombre_de_cages = models.IntegerField(validators=[MinValueValidator(0)])
    Argent_initial = models.FloatField(validators=[MinValueValidator(0)])
    Nourriture_disponible = models.IntegerField(validators=[MinValueValidator(0)], default =0)
    Nombre_de_femelles_en_gestation = models.IntegerField(validators=[MinValueValidator(0)],default = 0)


    def __str__(self):
        return self.Nom_de_mon_elevage
    
class Individu(models.Model):
    SEXE_CHOIX = [
        ('M', 'Mâle'),
        ('F', 'Femelle'),
    ]
    ETAT_CHOIX = [
        ('P', 'Présent'),
        ('V', 'Vendu'),
        ('M', 'Mort'),
        ('G', 'Gravide'),
    ]

    elevage = models.ForeignKey("Elevage", on_delete=models.CASCADE)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOIX)
    age = models.IntegerField()
    etat = models.CharField(max_length=1, choices=ETAT_CHOIX)

    def __str__(self):
        return f"{self.get_sexe_display()} - {self.age} mois - {self.get_etat_display()}"
    
    
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