# Generated by Django 4.2 on 2025-04-11 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lap1', '0003_elevage_nombre_de_femelles_en_gestation_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elevage',
            old_name='Quantité_de_nourriture_initiale',
            new_name='Quantite_de_nourriture',
        ),
        migrations.AlterField(
            model_name='elevage',
            name='Nombre_de_femelles_en_gestation',
            field=models.IntegerField(),
        ),
    ]
