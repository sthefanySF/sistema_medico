# Generated by Django 5.0.1 on 2024-04-04 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0018_remove_administrativo_orgao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='sexo',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1),
        ),
    ]
