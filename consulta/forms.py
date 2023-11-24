from django import forms
from .models import Paciente
from .models import Administrativo
from .models import Agendamento, Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'data_nascimento', 'email', 'rg', 'cpf', 'sexo', 'matricula', 'tipo_paciente', 'cargo_funcao', 'cep', 'cidade', 'bairro', 'uf', 'numero', 'ddd_telefone', 'complemento']

        
        
        labels = {
            'data_nascimento': 'Data de Nascimento',
            'tipo_paciente': 'Tipo de Paciente',
            'cargo_funcao': 'Cargo/Função',
            'ddd_telefone': 'DDD Telefone',
        }
        
        
        
        widgets = {
            'sexo': forms.RadioSelect(choices=Paciente.SEXO_CHOICES),
        }

        
        
class AdministrativoForm(forms.ModelForm):
    class Meta:
        model = Administrativo
        fields = ['nome', 'data_nascimento', 'email', 'rg', 'cpf', 'sexo', 'matricula_siape', 'cargo_funcao', 'cep', 'cidade', 'bairro', 'uf', 'numero', 'ddd_telefone', 'complemento','orgao','lotacao_de_exercicio']

        
        
        labels = {
            'data_nascimento': 'Data de Nascimento',
            'cargo_funcao': 'Cargo/Função',
            'ddd_telefone': 'DDD Telefone',
            'lotacao_de_exercicio':'Lotação de Exercício',
            'matricula_siape': 'Matrícula SIAPE',
        }
        
        
        
        widgets = {
            'sexo': forms.RadioSelect(choices=Administrativo.SEXO_CHOICES),}

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['paciente', 'medico', 'data_agendamento', 'prioridade_atendimento']

        labels = {
            'data_agendamento': 'Data do Agendamento',
            'prioridade_atendimento': 'Prioridade de Atendimento',
        }

        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'medico': forms.Select(attrs={'class': 'form-control'}),
            'data_agendamento': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'prioridade_atendimento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }