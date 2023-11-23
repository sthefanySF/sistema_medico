from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *
# Register your models here.


class CampoPaciente(admin.ModelAdmin):
    search_fields = ['nome']
    list_display = ('nome',)



class CampoFilaEspera(admin.ModelAdmin):
    search_fields = ['paciente']
    
class CampoAdministrativo(admin.ModelAdmin):
    search_fields = ['nome']
    list_display = ('nome', 'email', 'matricula_siape','orgao',)




admin.site.register(Paciente, CampoPaciente)
admin.site.register(FilaEspera, CampoFilaEspera)
admin.site.register(Administrativo,CampoAdministrativo)