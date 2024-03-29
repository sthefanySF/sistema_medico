# Generated by Django 5.0.1 on 2024-03-25 17:10

import consulta.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0014_alter_administrativo_cpf_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='administrativo',
            options={'ordering': ['nome'], 'verbose_name': 'Administrativo', 'verbose_name_plural': 'Administrativo'},
        ),
        migrations.AlterField(
            model_name='administrativo',
            name='cpf',
            field=models.CharField(max_length=14, validators=[consulta.models.validate_cpf, django.core.validators.MinLengthValidator(11)]),
        ),
        migrations.AlterField(
            model_name='administrativo',
            name='data_nascimento',
            field=models.DateField(validators=[consulta.models.data_nasc_valida], verbose_name='Data de nascimento'),
        ),
        migrations.AlterField(
            model_name='administrativo',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='administrativo',
            name='nome',
            field=models.CharField(max_length=100, verbose_name='Nome Completo'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='cpf',
            field=models.CharField(max_length=14, validators=[consulta.models.validate_cpf, django.core.validators.MinLengthValidator(11)]),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='data_nascimento',
            field=models.DateField(validators=[consulta.models.data_nasc_valida], verbose_name='Data de Nascimento'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='uf',
            field=models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AM', 'Amazonas'), ('AP', 'Amapá'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MG', 'Minas Gerais'), ('MS', 'Mato Grosso do Sul'), ('MT', 'Mato Grosso'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('PR', 'Paraná'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('RS', 'Rio Grande do Sul'), ('SC', 'Santa Catarina'), ('SE', 'Sergipe'), ('SP', 'São Paulo'), ('TO', 'Tocantins')], default='AC', max_length=2, verbose_name='UF'),
        ),
        migrations.AlterField(
            model_name='profissionaldasaude',
            name='cpf',
            field=models.CharField(max_length=14, validators=[consulta.models.validate_cpf, django.core.validators.MinLengthValidator(11)]),
        ),
        migrations.AlterField(
            model_name='profissionaldasaude',
            name='data_nascimento',
            field=models.DateField(validators=[consulta.models.data_nasc_valida], verbose_name='Data de Nascimento'),
        ),
    ]
