# Generated by Django 4.2.7 on 2023-11-22 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='rg',
            field=models.CharField(default='', max_length=20),
        ),
    ]
