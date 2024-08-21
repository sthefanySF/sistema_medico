import consulta.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0043_laudo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArquivoPaciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(upload_to=consulta.models.file_up)),
                ('data_envio', models.DateTimeField(auto_now_add=True)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consulta.paciente')),
            ],
            options={
                'ordering': ['paciente', 'data_envio'],
            },
        ),
    ]
