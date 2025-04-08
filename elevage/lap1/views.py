from django.shortcuts import render
from .models import Elevage, Individu

def liste(request):
    elevages = Elevage.objects.all()
    return render(request, 'lap1/liste.html', {'elevages': elevages})

def elevage(request, elevage_id):
    elevage = Elevage.objects.get(id=elevage_id)
    individus = Individu.objects.filter(elevage=elevage)
    return render(request, 'lap1/elevage.html', {'elevage': elevage, 'individus': individus})

def nouveau(request):
    return 'yes'

def index(request):
    return render(request, 'lap1/index.html')

def regles(request):
    return render(request, 'lap1/regles.html')