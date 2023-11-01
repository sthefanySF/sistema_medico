from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *
# Register your models here.


class CampoPaciente(ModelAdmin):
    search_fields = ['nome']
    list_display = ('nome',)



class CampoFilaEspera(ModelAdmin):
    search_fields = ['paciente']





admin.site.register(Paciente, CampoPaciente)
admin.site.register(FilaEspera, CampoFilaEspera)