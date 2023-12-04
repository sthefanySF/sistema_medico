from django import forms
from .models import Paciente
from .models import Administrativo
from .models import Profissionaldasaude
from .models import Agendamento, Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'data_nascimento', 'email', 'rg', 'cpf', 'sexo', 'matricula', 'tipo_paciente', 'cargo_funcao','ddd_telefone',  'uf','cep', 'cidade', 'bairro',  'numero',  'complemento']

        
        
        labels = {
            'data_nascimento': 'Data de Nascimento',
            'tipo_paciente': 'Tipo de Paciente',
            'cargo_funcao': 'Cargo/Função',
            'ddd_telefone': 'DDD Telefone',
        }
        
        
        
        widgets = {
            'sexo': forms.RadioSelect(choices=[('M', 'Masculino'), ('F', 'Feminino')]),
        }

class PacienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'data_nascimento', 'email', 'rg', 'cpf', 'sexo', 'matricula', 'tipo_paciente', 'cargo_funcao', 'ddd_telefone', 'uf', 'cep', 'cidade', 'bairro', 'numero', 'complemento']

        labels = {
            'data_nascimento': 'Data de Nascimento',
            'tipo_paciente': 'Tipo de Paciente',
            'cargo_funcao': 'Cargo/Função',
            'ddd_telefone': 'DDD Telefone',
        }

        widgets = {
            'sexo': forms.RadioSelect(choices=[('M', 'Masculino'), ('F', 'Feminino')]),
        }
        
class AdministrativoForm(forms.ModelForm):
    class Meta:
        model = Administrativo
        fields = ['nome', 'data_nascimento', 'email', 'rg', 'cpf', 'sexo', 'matricula_siape', 'cargo_funcao','orgao','lotacao_de_exercicio', 'ddd_telefone','uf','cep', 'cidade', 'bairro',  'numero',  'complemento']

        
        
        labels = {
            'data_nascimento': 'Data de Nascimento',
            'cargo_funcao': 'Cargo/Função',
            'ddd_telefone': 'DDD Telefone',
            'lotacao_de_exercicio':'Lotação de Exercício',
            'matricula_siape': 'Matrícula SIAPE',
        }
        
        
        
        widgets = {
            'sexo': forms.RadioSelect(choices=[('M', 'Masculino'), ('F', 'Feminino')]),
        }

class Profissionaldasaude(forms.ModelForm):
    class Meta:
        model = Profissionaldasaude
        fields = ['nome', 'data_nascimento', 'email', 'rg', 'cpf', 'sexo', 'identificacao_unica', 'area','unidade_siass','formacao','conselho','registro', 'ddd_telefone','uf','cep', 'cidade', 'bairro',  'numero',  'complemento']

        
        
        labels = {
            'data_nascimento': 'Data de Nascimento',
            'identificacao_unica': 'Identificação Única',
            'ddd_telefone': 'DDD Telefone',
            'unidade_siass':'Unidade SIASS',
          
        }
        
        
        
        widgets = {
            'sexo': forms.RadioSelect(choices=[('M', 'Masculino'), ('F', 'Feminino')]),
        }


class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['paciente', 'profissional_saude', 'data_agendamento', 'prioridade_atendimento']

        labels = {
            'data_agendamento': 'Data do Agendamento',
            'prioridade_atendimento': 'Prioridade de Atendimento',
        }

        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'profissional_saude': forms.Select(attrs={'class': 'form-control'}),
            'data_agendamento': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'prioridade_atendimento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }