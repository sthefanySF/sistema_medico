from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *
# Register your models here.


class CampoPaciente(admin.ModelAdmin):
    search_fields = ['nome']
    list_display = ('nome', 'data_nascimento', 'email')



class CampoAdministrativo(admin.ModelAdmin):
    search_fields = ['nome']
    list_display = ('nome', 'data_nascimento','email')


class CampoProfissionaldasaude(admin.ModelAdmin):
    search_fields = ['nome']
    list_display = ('nome', 'data_nascimento', 'email')


class CampoAgendamento(admin.ModelAdmin):
    search_fields = ['paciente']
    list_display = ('paciente', 'data_agendamento')  

class CampoAtendimento(admin.ModelAdmin):
    search_fields = ['paciente__nome']  # Substitua 'paciente__nome' pelo campo correto
    list_display = ('paciente', 'data_atendimento', 'anamnese', 'exame_fisico')    


admin.site.register(Paciente, CampoPaciente)
admin.site.register(Administrativo, CampoAdministrativo)
admin.site.register(Profissionaldasaude, CampoProfissionaldasaude)
admin.site.register(Agendamento, CampoAgendamento)
admin.site.register(Atendimento, CampoAtendimento)