

from datetime import datetime
from datetime import date
from django.utils.timezone import now
from django.utils import timezone
from django import forms
import json
from .models import Atendimento, Administrativo, AtestadoMedico, Profissionaldasaude, Agendamento, Paciente, ReceitaMedica
from django.contrib.auth.models import User
from .choices import UF_CHOICE


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
            'nome_social': 'Nome Social', 
        }
        
        
        
        widgets = {
            'sexo': forms.Select(choices=Paciente.SEXO_CHOICES),
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
        fields = '__all__'
        
        labels = {
            'data_nascimento': 'Data de Nascimento',
            'cargo_funcao': 'Cargo/Função',
            'ddd_telefone': 'DDD Telefone',
            'lotacao_de_exercicio': 'Lotação de Exercício',
            'matricula_siape': 'Matrícula SIAPE',
            'nome_social': 'Nome Social' 
        }
        
        widgets = {
            'sexo': forms.Select(choices=Administrativo.SEXO_CHOICES),
            'uf': forms.Select(choices=UF_CHOICE),  # Certifique-se de incluir o widget correto
        }

    def __init__(self, *args, **kwargs):
        super(AdministrativoForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control'

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento > datetime.now().date():
            raise forms.ValidationError('Informe uma data válida.')
        return data_nascimento


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
        data_agendamento = self.cleaned_data.get('data_agendamento')

        # Verifica se data_agendamento não é None
        if data_agendamento is None:
            raise forms.ValidationError("A data do agendamento é obrigatória.")

        # Obtenha a data atual no fuso horário local
        hoje = timezone.localtime().date()

        # Imprime as datas para diagnóstico
        print(f"Data do agendamento: {data_agendamento}, Data de hoje: {hoje}")

        # Comparação de datas sem considerar hora
        if data_agendamento < hoje:
            raise forms.ValidationError("Data incorreta! Ajuste a data do agendamento e tente novamente.")

        return data_agendamento

    class Meta:
        model = Agendamento
        exclude = ['id']

        labels = {
            'data_agendamento': 'Data do Agendamento',
            'prioridade_atendimento': 'Prioridade de Atendimento',
        }

        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'profissional_saude': forms.Select(attrs={'class': 'form-control'}),
            'data_agendamento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'turno': forms.Select(attrs={'class': 'form-control'}), 
            'prioridade_atendimento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status_atendimento': forms.HiddenInput(attrs={'value': 'pendente'}), 
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
    class Meta:
        model = AtestadoMedico
        fields = ['dias_afastamento', 'cid', 'texto_padrao']

    def __init__(self, *args, **kwargs):
        agendamento = kwargs.pop('agendamento', None)
        super(AtestadoMedicoForm, self).__init__(*args, **kwargs)

        if agendamento:
            self.fields['paciente'] = forms.CharField(
                initial=agendamento.paciente.nome, label="Paciente", disabled=True, required=False)
            self.fields['profissional'] = forms.CharField(
                initial=agendamento.profissional_saude.nome, label="Profissional de Saúde", disabled=True, required=False)
            self.fields['data_agendamento'] = forms.CharField(
                initial=agendamento.data_agendamento.strftime('%Y-%m-%d %H:%M'), label="Data do Agendamento", disabled=True, required=False)
            self.fields['data_criacao'] = forms.CharField(
                initial=timezone.now().strftime('%Y-%m-%d %H:%M'), label="Data de Criação", disabled=True, required=False)

        self.fields['texto_padrao'].required = False

class ReceitaMedicaForm(forms.ModelForm):
    class Meta:
        model = ReceitaMedica
        fields = ['prescricao', 'dosagem', 'via_administrativa', 'modo_uso', 'tipo']

    def __init__(self, *args, **kwargs):
        agendamento = kwargs.pop('agendamento', None)
        super().__init__(*args, **kwargs)
        
        if agendamento:
            self.fields['paciente_nome'] = forms.CharField(
                initial=agendamento.paciente.nome, label="Paciente", disabled=True, required=False)
            self.fields['profissional'] = forms.CharField(
                initial=agendamento.profissional_saude.nome, label="Profissional de Saúde", disabled=True, required=False)
            self.fields['data_agendamento'] = forms.CharField(
                initial=agendamento.data_agendamento.strftime('%Y-%m-%d %H:%M'), label="Data do Agendamento", disabled=True, required=False)
            self.fields['data_criacao'] = forms.CharField(
                initial=timezone.now().strftime('%Y-%m-%d %H:%M'), label="Data de Criação", disabled=True, required=False)
        
        for field in self.fields:
            self.fields[field].required = False
            
        # for f in self.fields:
        #     self.fields[f].widget.attrs['class'] = 'input'