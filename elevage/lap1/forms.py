from django import forms
from .models import Elevage

class DébutForm(forms.ModelForm):
    class Meta: 
#usage d'une classe meta? pour le modèle
        model = Elevage
        fields = ['name', 'number_lapins', 'food_quantity', 'number_cages', 'money']


class ActionForm(forms.Form):
    sale_lapins = forms.IntegerField(label='Nombre de lapins à vendre')
    achat_nourriture = forms.FloatField(label='Quantité de nourriture à acheter')
