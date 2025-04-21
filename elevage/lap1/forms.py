from django import forms
from .models import Elevage

class DebutForm(forms.ModelForm):
    class Meta: 
#usage d'une classe meta? pour le modèle
        model = Elevage
        fields = ['Nom_de_mon_elevage', 'Nombre_de_lapins_males', 'Nombre_de_lapins_femelles', 'Nombre_de_cages', 'Nourriture_disponible','Argent_initial']

    Argent_initial = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'step': 100}),
        label="Argent initial"
    )

    Nourriture_disponible = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'step': 250}),
        label="Nourriture disponible"
    )

from django import forms

class ActionForm(forms.Form):
    sale_lapins = forms.IntegerField(label='Nombre de lapins mâles à vendre', min_value=0)
    sale_lapins2 = forms.IntegerField(label='Nombre de lapins femelles à vendre', min_value=0)
    achat_nourriture = forms.IntegerField(
        label='Quantité de nourriture à acheter (en g)',
        min_value=0,
        widget=forms.NumberInput(attrs={'step': 250})
    )
    gestation = forms.IntegerField(label='Nombre de femelles entrant en gestation', min_value=0)
    achat_femelles = forms.IntegerField(label='Nombre de femelles à acheter', min_value=0)
    achat_males = forms.IntegerField(label='Nombre de males entrant en gestation', min_value=0)
