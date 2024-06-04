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
    search_fields = ['nome', 'cpf']
    list_display = ('nome', 'data_nascimento', 'email')


class CampoAgendamento(admin.ModelAdmin):
    search_fields = ['paciente__nome', 'paciente__cpf']
    list_display = ('paciente', 'data_agendamento', 'nome_profissional')

    #  Função para exibir um campo que não é diretamente acessível no modelo em si,
    #  mas sim através de uma relação com outro modelo. No caso, o modelo agendamento e o modelo PRofissional
    def nome_profissional(self, n):
        return n.profissional_saude.nome
    nome_profissional.short_description = 'Profissional'



class CampoAtendimento(admin.ModelAdmin):
    search_fields = ['paciente__nome']  # Substitua 'paciente__nome' pelo campo correto
    list_display = ('paciente', 'data_atendimento', 'anamnese', 'exame_fisico')    


class CampoAtestadoMedico(admin.ModelAdmin):
    search_fields = ['agendamento__paciente__nome', 'cid']
    list_display = ('paciente', 'data_consulta', 'dias_afastamento', 'cid')

    def paciente(self, obj):
        return obj.agendamento.paciente.nome
    paciente.short_description = 'Paciente'

    def data_consulta(self, obj):
        return obj.agendamento.data_agendamento
    data_consulta.short_description = 'Data da Consulta'

admin.site.register(Paciente, CampoPaciente)
admin.site.register(Administrativo, CampoAdministrativo)
admin.site.register(Profissionaldasaude, CampoProfissionaldasaude)
admin.site.register(Agendamento, CampoAgendamento)
admin.site.register(Atendimento, CampoAtendimento)
admin.site.register(AtestadoMedico, CampoAtestadoMedico)