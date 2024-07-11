# Generated by Django 5.0.1 on 2024-06-18 13:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0032_remove_atendimento_cid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceitaMedica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_receita', models.DateTimeField(auto_now_add=True)),
                ('prescricao', models.TextField()),
                ('dosagem', models.CharField(max_length=100)),
                ('via_administrativa', models.CharField(max_length=100)),
                ('modo_uso', models.CharField(max_length=100)),
                ('agendamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receitas', to='consulta.agendamento')),
            ],
            options={
                'verbose_name': 'Receita Médica',
                'verbose_name_plural': 'Receitas Médicas',
                'ordering': ['-data_receita'],
            },
        ),
    ]
