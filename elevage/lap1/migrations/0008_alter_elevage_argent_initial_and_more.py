# Generated by Django 4.2 on 2025-04-17 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lap1', '0007_alter_elevage_argent_initial_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elevage',
            name='Argent_initial',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='elevage',
            name='Nombre_de_cages',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='elevage',
            name='Nombre_de_femelles_en_gestation',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='elevage',
            name='Nombre_de_lapins_femelles',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='elevage',
            name='Nombre_de_lapins_males',
            field=models.IntegerField(),
        ),
    ]
