# Generated by Django 5.0.1 on 2024-04-04 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0020_alter_paciente_ddd_telefone'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArquivoExame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(upload_to='exames_pdfs/')),
            ],
        ),
        migrations.RemoveField(
            model_name='atendimento',
            name='pdf_exames',
        ),
        migrations.AddField(
            model_name='atendimento',
            name='pdf_exames',
            field=models.ManyToManyField(blank=True, to='consulta.arquivoexame'),
        ),
    ]
