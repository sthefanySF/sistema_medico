

from datetime import datetime
from django.utils import timezone
from django import forms
import json
from .models import Atendimento, Administrativo, AtestadoMedico, Profissionaldasaude, Agendamento, Paciente
from django.contrib.auth.models import User


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        #fields = ['nome', 'data_nascimento', 'email', 'rg', 'cpf', 'sexo', 'matricula', 'tipo_paciente', 'cargo_funcao','ddd_telefone',  'uf','cep', 'cidade', 'bairro',  'numero',  'complemento']
        fields = '__all__'
        
        
        labels = {
            'data_nascimento': 'Data de Nascimento',
            'tipo_paciente': 'Tipo de Paciente',
            'cargo_funcao': 'Cargo/Função',
            'ddd_telefone': 'DDD Telefone',
        }
        
        
        
        widgets = {
            'sexo': forms.Select(choices=[('M', 'Masculino'), ('F', 'Feminino')]),
            'tipo_paciente': forms.Select(choices=Paciente.TIPO_PACIENTE_CHOICES),
        }
        
    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        # self.fields['data_nascimento'].error_messages = {'required': 'Email é um campo obrigatório.'}

        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control'

    def clean_data_nascimento(self):
        data_nascimeto = self.cleaned_data.get('data_nascimento')
        if data_nascimeto > datetime.now().date():
            raise forms.ValidationError('Informe uma data válida.')
        return data_nascimeto
    


        
class AdministrativoForm(forms.ModelForm):
    class Meta:
        model = Administrativo
        # fields = ['nome', 'data_nascimento', 'email', 'rg', 'cpf', 'sexo', 'matricula_siape', 'cargo_funcao','orgao',
        #           'lotacao_de_exercicio', 'ddd_telefone','uf','cep', 'cidade', 'bairro',  'numero',  'complemento']
        fields = '__all__'
        
        
        labels = {
            'data_nascimento': 'Data de Nascimento',
            'cargo_funcao': 'Cargo/Função',
            'ddd_telefone': 'DDD Telefone',
            'lotacao_de_exercicio':'Lotação de Exercício',
            'matricula_siape': 'Matrícula SIAPE',
        }
        
        
        
        widgets = {
            'sexo': forms.Select(choices=[('M', 'Masculino'), ('F', 'Feminino')]),
        }


    def __init__(self, *args, **kwargs):
        super(AdministrativoForm, self).__init__(*args, **kwargs)
        # self.fields['data_nascimento'].error_messages = {'required': 'Email é um campo obrigatório.'}

        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control'

    def clean_data_nascimento(self):
        data_nascimeto = self.cleaned_data.get('data_nascimento')
        if data_nascimeto > datetime.now().date():
            raise forms.ValidationError('Informe uma data válida.')
        return data_nascimeto


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         # fields = ('username', 'email', 'password', 'confirme_senha')
#         fields = ('username',)


class ProfissionaldasaudeForm(forms.ModelForm):
    class Meta:
        model = Profissionaldasaude

        # exclude = ('usuario',)
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProfissionaldasaudeForm, self).__init__(*args, **kwargs)

        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control'


    # Verifica se a data de nascimento não é menor que a data atual
    def clean_data_nascimento(self):
        data_nascimeto = self.cleaned_data.get('data_nascimento')
        if data_nascimeto > datetime.now().date():
            raise forms.ValidationError('Informe uma data válida.')
        return data_nascimeto



class AgendamentoForm(forms.ModelForm):
    def clean_data_agendamento(self):
        # Obtém a data de agendamento do formulário
        data_agendamento = self.cleaned_data.get('data_agendamento')
        
        # Verifica se a data de agendamento é no passado
        if data_agendamento.date() < datetime.now().date():

            # Se for no passado, levanta uma exceção de ValidationError
            raise forms.ValidationError("A data do agendamento não pode ser no passado.")
        
        # Retorna a data de agendamento se tudo estiver válido
        return data_agendamento

    class Meta:
        model = Agendamento
        exclude = ['id']  # Exclui o campo 'id' do formulário

        labels = {
            'data_agendamento': 'Data do Agendamento',
            'prioridade_atendimento': 'Prioridade de Atendimento',
        }

        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'profissional_saude': forms.Select(attrs={'class': 'form-control'}),
            'data_agendamento': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'turno': forms.Select(attrs={'class': 'form-control'}),  # Adicione esta linha
            'prioridade_atendimento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status_atendimento': forms.HiddenInput(attrs={'value': 'pendente'}),  # Defina o valor padrão aqui
        }




class AgendamentoReagendarForm(forms.ModelForm):
    def clean_data_agendamento(self):
        data_agendamento = self.cleaned_data.get('data_agendamento')

        if data_agendamento.date() < datetime.now().date():
            raise forms.ValidationError("A data do reagendamento não pode ser no passado.")

        return data_agendamento


    class Meta:
        model = Agendamento
        fields = ['profissional_saude', 'data_agendamento', 'prioridade_atendimento', 'turno']

        labels = {
            'profissional_saude': 'Selecionar profissional de saúde:',
            'data_agendamento': 'Selecionar nova data:',
            'prioridade_atendimento': 'Prioridade de Atendimento',
        }

        widgets = {
            'profissional_saude': forms.Select(attrs={'class': 'form-control'}),
            'data_agendamento': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'turno': forms.Select(attrs={'class': 'form-control'}),
            'prioridade_atendimento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    



class JustificativaCancelamentoForm(forms.Form):
    justificativa = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Digite a justificativa aqui'}))


class AtendimentoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = ['anamnese', 'exame_fisico', 'exames_complementares', 'pdf_exames', 'diagnostico', 'conduta']
        
class AtestadoMedicoForm(forms.ModelForm):
    # Definição dos campos não relacionados ao modelo
    paciente = forms.CharField(label="Paciente", disabled=True, required=False)  # Campo para o nome do paciente
    profissional = forms.CharField(label="Profissional de Saúde", disabled=True, required=False)  # Campo para o nome do profissional de saúde
    data_agendamento = forms.CharField(label="Data do Agendamento", disabled=True, required=False)  # Campo para a data do agendamento
    data_criacao = forms.CharField(label="Data de Criação", disabled=True, required=False)  # Campo para a data de criação

    class Meta:
        model = AtestadoMedico
        fields = ['dias_afastamento', 'cid']  # Campos do modelo que serão incluídos no formulário

    def __init__(self, *args, **kwargs):
        agendamento = kwargs.pop('agendamento', None)  # Extrai o objeto 'agendamento' dos argumentos passados
        super(AtestadoMedicoForm, self).__init__(*args, **kwargs)  # Chama o construtor da classe pai

        # Preenche os campos com informações do agendamento, se fornecido
        if agendamento:
            self.fields['paciente'].initial = agendamento.paciente.nome  # Preenche o campo do paciente com o nome do paciente do agendamento
            self.fields['profissional'].initial = agendamento.profissional_saude.nome  # Preenche o campo do profissional com o nome do profissional do agendamento
            self.fields['data_agendamento'].initial = agendamento.data_agendamento.strftime('%Y-%m-%d %H:%M')  # Preenche o campo da data do agendamento com a data formatada do agendamento
            self.fields['data_criacao'].initial = timezone.now().strftime('%Y-%m-%d %H:%M')  # Preenche o campo da data de criação com a data e hora atuais
