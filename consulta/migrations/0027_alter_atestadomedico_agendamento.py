# Generated by Django 5.0.1 on 2024-06-03 14:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0026_alter_atestadomedico_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atestadomedico',
            name='agendamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='atestados', to='consulta.agendamento'),
        ),
    ]
