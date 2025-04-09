from django import forms
from .models import Elevage

class DebutForm(forms.ModelForm):
    class Meta: 
#usage d'une classe meta? pour le modèle
        model = Elevage
        fields = ['Nom_de_mon_elevage', 'Nombre_de_lapins_males', 'Nombre_de_lapins_femelles', 'Quantité_de_nourriture_initiale', 'Nombre_de_cages', 'Argent_initial']


class ActionForm(forms.Form):
    class Meta:
        sale_lapins = forms.IntegerField(label='Nombre de lapins à vendre')
        achat_nourriture = forms.FloatField(label='Quantité de nourriture à acheter')
