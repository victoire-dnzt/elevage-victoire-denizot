from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('liste/', views.liste, name='liste'),
    path('elevage/<int:elevage_id>/', views.elevage, name='elevage'),
    path('regles/', views.regles, name='regles'),
    path('nouveau/', views.new_elevage, name='nouveau'),
    path('menu/', views.menu, name='menu'),
    path('actions/<int:elevage_id>/', views.actions, name='actions')
]

