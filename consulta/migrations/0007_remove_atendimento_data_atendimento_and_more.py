# Generated by Django 4.2.7 on 2024-01-15 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0006_atendimento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atendimento',
            name='data_atendimento',
        ),
        migrations.RemoveField(
            model_name='atendimento',
            name='paciente',
        ),
        migrations.RemoveField(
            model_name='atendimento',
            name='profissional_saude',
        ),
        migrations.AddField(
            model_name='atendimento',
            name='agendamento',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='consulta.agendamento'),
            preserve_default=False,
        ),
    ]
