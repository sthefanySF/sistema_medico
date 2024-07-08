from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')

    # Lista de nomes de grupos que você deseja criar
    group_names = ['administrativo', 'profissionais de saude', 'administradores']

    for group_name in group_names:
        Group.objects.get_or_create(name=group_name)

class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0033_receitamedica'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]