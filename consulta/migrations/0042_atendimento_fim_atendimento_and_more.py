# Generated by Django 5.0.1 on 2024-08-12 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0041_alter_agendamento_data_agendamento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='atendimento',
            name='fim_atendimento',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='atendimento',
            name='inicio_atendimento',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]