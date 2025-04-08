from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nouveau/', views.nouveau, name='nouveau'),
    path('liste/', views.liste, name='liste'),
    path('elevage/<int:elevage_id>/', views.elevage, name='elevage'),
    path('regles', views.regles, name='regles')
]