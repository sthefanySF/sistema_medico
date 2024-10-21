
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User

from consulta.choices import *

from validate_docbr import CPF
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.utils import timezone


def validate_cpf(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise ValidationError('CPF inválido.')


def data_nasc_valida(value):
    if value > datetime.now().date():
        raise ValidationError('Informe uma data de nascimento válida.')


def arquivos_upload(instance, filename, k):
  import os
  ext = filename.split('.')[-1]
  i = 0
  fn = '/'.join(['arquivos', str(instance.paciente.cpf.replace('.','').replace('-',''))+'_0'+str(k)+'_S'+str(i)+'.'+ext])
  while os.path.exists(MEDIA_ROOT+fn):
    i = i + 1
    fn = '/'.join(['arquivos', str(instance.paciente.cpf.replace('.','').replace('-',''))+'_0'+str(k)+'_S'+str(i)+'.'+ext])
  return fn


def file_up(instance, filename):
  return arquivos_upload(instance, filename, 'arquivo')


class Paciente(models.Model):

    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro') 
    ]
    
    nome = models.CharField(max_length=100)
    nome_social = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nome Social')  
    data_nascimento = models.DateField(verbose_name='Data de Nascimento', validators=[data_nasc_valida], blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14, validators=[validate_cpf, MinLengthValidator(11)])
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    matricula = models.CharField(max_length=20)
    TIPO_PACIENTE_CHOICES = [
        ('Aluno', 'Aluno'),
        ('Servidor', 'Servidor'),
        ('Outro', 'Outro'),
    ]

    tipo_paciente = models.CharField(max_length=20, choices=TIPO_PACIENTE_CHOICES)
    cargo_funcao = models.CharField(max_length=50, default='', blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=50, default='', blank=True, null=True)
    uf = models.CharField('UF', max_length=2, choices=UF_CHOICE, default='AC', blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    ddd_telefone = models.CharField(max_length=8)
    complemento = models.CharField(max_length=100, blank=True, null=True, default='')  # Adicionando o valor padrão aqui

    def save(self, *args, **kwargs):
        # Se o sexo não for fornecido, defina-o como None
        if not self.sexo:
            self.sexo = None
        super().save(*args, **kwargs)


    def __str__(self):
        return self.get_display_name()
    
    def get_display_name(self):
        return self.nome_social if self.nome_social else self.nome
    
    def idade(self):
        today = date.today()
        age = today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return age 

def validate_unique_cpf(value):
    if Administrativo.objects.filter(cpf=value).exists():
        raise ValidationError('CPF já cadastrado.')

def validate_unique_email(value):
    if Administrativo.objects.filter(email=value).exists():
        raise ValidationError('Email já cadastrado.')

class Administrativo(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro') 
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    nome = models.CharField(max_length=100, verbose_name='Nome Completo')
    nome_social = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nome Social')  
    data_nascimento = models.DateField(verbose_name='Data de nascimento', validators=[data_nasc_valida])
    email = models.EmailField()
    rg = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, validators=[validate_cpf, MinLengthValidator(11)])
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    cargo_funcao = models.CharField(max_length=50, default='')
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50, default='')
    uf = models.CharField('UF', max_length=2, choices=UF_CHOICE, default='AC')
    numero = models.CharField(max_length=10)
    ddd_telefone = models.CharField('Telefone Celular', max_length=14, help_text='Com DDD.')
    complemento = models.CharField(max_length=100, blank=True, null=True, default='')
    lotacao_de_exercicio = models.CharField(max_length=50, default='')
    matricula_siape = models.CharField(max_length=20)

    def __str__(self):
        return self.get_display_name()
    
    def get_display_name(self):
        return self.nome_social if self.nome_social else self.nome
    
    def idade(self):
        today = date.today()
        age = today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return age 

    class Meta:
        ordering = ['-nome']
        verbose_name = 'Administrativo'
        verbose_name_plural = 'Administrativo'

    
class Profissionaldasaude(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro') 
    ]
    usuario = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    nome = models.CharField('Nome Completo', max_length=100)
    nome_social = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nome Social')  
    data_nascimento = models.DateField(u'Data de Nascimento', validators=[data_nasc_valida])
    email = models.EmailField()
    rg = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, validators=[validate_cpf, MinLengthValidator(11)])
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    identificacao_unica = models.CharField(max_length=50, default='')
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50, default='')
    uf = models.CharField('UF', max_length=2, choices=UF_CHOICE, default='AC')
    numero = models.CharField(max_length=10)
    ddd_telefone = models.CharField('Telefone Celular', max_length=14, help_text='Com DDD.')
    complemento = models.CharField(max_length=100, blank=True, null=True, default='') # blank=True, null=True é pra dizer que não é obrigatorio 
    area = models.CharField(max_length=50, default='')
    unidade_siass = models.CharField(max_length=50, default='')
    formacao = models.CharField(max_length=20)
    conselho = models.CharField(max_length=20)
    registro = models.CharField(max_length=20)


    def __str__(self):
        return self.get_display_name()
    
    def get_display_name(self):
        return self.nome_social if self.nome_social else self.nome
    
    def idade(self):
        today = date.today()
        age = today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return age 

    class Meta:
        # db_table = 'PROFISSIONALDASAUDE'
        ordering = ['nome', ]
        verbose_name = 'Profissonal de saúde'
        verbose_name_plural = 'Profissonais de saúde'


class Agendamento(models.Model):
    TURNO_CHOICES = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
    ]

    status_atendimento = models.CharField(max_length=20, choices=[
        ('confirmado', 'Confirmado'),
        ('ausente', 'Ausente'),
        ('pendente', 'Pendente'),
        ('cancelado', 'Cancelado'),
        ('atendido', 'Atendido'),
    ], default='pendente')
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    profissional_saude = models.ForeignKey('Profissionaldasaude', on_delete=models.CASCADE)
    data_agendamento = models.DateField('Data Agendamento', blank=False, null=False)
    turno = models.CharField(max_length=10, choices=TURNO_CHOICES)
    prioridade_atendimento = models.BooleanField(default=False)
    justificativa_cancelamento = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Agendamento para {self.paciente.nome}"

    def atualizar_status(self):
        now = timezone.now().date()
        
        # Garantir que data_agendamento não é None antes de comparar
        if self.data_agendamento and self.data_agendamento < now:
            if self.status_atendimento not in ['atendido', 'confirmado']:
                self.status_atendimento = 'ausente'
            self.save()

    class Meta:
        ordering = ['-data_agendamento', 'paciente__nome']
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'


class Atendimento(models.Model):
    agendamento = models.OneToOneField('Agendamento', on_delete=models.CASCADE)
    anamnese = models.TextField()
    exame_fisico = models.TextField()
    exames_complementares = models.TextField()
    pdf_exames = models.FileField(upload_to='exames_pdfs/', null=True, blank=True)
    diagnostico = models.TextField()
    conduta = models.TextField()
    inicio_atendimento = models.DateTimeField(null=True, blank=True)
    fim_atendimento = models.DateTimeField(null=True, blank=True)
    medico_responsavel = models.ForeignKey(User, on_delete=models.CASCADE, related_name='atendimentos', null=True, blank=True)
    privado = models.BooleanField(default=False)  # Campo para marcar se a consulta é privada
    medico_logado = models.ForeignKey(Profissionaldasaude, related_name='atendimentos_realizados', on_delete=models.SET_NULL, null=True)

    @property
    def profissional_saude(self):
        return self.agendamento.profissional_saude

    @property
    def paciente(self):
        return self.agendamento.paciente

    @property
    def data_atendimento(self):
        return self.agendamento.data_agendamento

    def __str__(self):
        return f"Atendimento para {self.paciente.nome} em {self.data_atendimento}"

    @property
    def duracao_atendimento(self):
        if self.inicio_atendimento and self.fim_atendimento:
            return self.fim_atendimento - self.inicio_atendimento
        return None

    class Meta:
        ordering = ['agendamento']


class ArquivoPaciente(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to=file_up)
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Arquivo de {self.paciente.nome}"

    class Meta:
        ordering = ['paciente', 'data_envio']


class AtestadoMedico(models.Model):
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, related_name='atestados')
    dias_afastamento = models.IntegerField()
    cid = models.CharField(max_length=10)
    texto_padrao = models.TextField(default='Atesto que o(a) paciente esteve em consulta no dia {{ data_consulta }}, e necessita de [[DIAS]] dias de afastamento de suas atividades normais, para sua convalescença.')
    data_criacao = models.DateTimeField(auto_now_add=True)

    @property
    def paciente(self):
        return self.agendamento.paciente
    
    @property
    def data_consulta(self):
        return self.agendamento.data_agendamento

    @property
    def profissional(self):
        return self.agendamento.profissional_saude

    def __str__(self):
        return f"Atestado Médico para {self.paciente.nome} em {self.data_consulta}"

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Atestado Médico'
        verbose_name_plural = 'Atestados Médicos'

        
class ReceitaMedica(models.Model):
    TIPO_CHOICES = (
        ('simples', 'Simples'),
        ('controle_especial', 'Controle Especial'),
    )
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, related_name='receitas')
    data_receita = models.DateTimeField(auto_now_add=True)
    prescricao = models.TextField()
    dosagem = models.CharField(max_length=100)
    via_administrativa = models.CharField(max_length=100)
    modo_uso = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='simples')

    @property
    def paciente(self):
        return self.agendamento.paciente
    
    @property
    def data_consulta(self):
        return self.agendamento.data_agendamento

    @property
    def profissional(self):
        return self.agendamento.profissional_saude

    def __str__(self):
        return f"Receita Médica para {self.paciente.nome} em {self.data_consulta}"

    class Meta:
        ordering = ['-data_receita']
        verbose_name = 'Receita Médica'
        verbose_name_plural = 'Receitas Médicas'


class Laudo(models.Model):
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, related_name='laudos')
    data_laudo = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField()

    @property
    def paciente(self):
        return self.agendamento.paciente

    @property
    def data_consulta(self):
        return self.agendamento.data_agendamento

    @property
    def profissional(self):
        return self.agendamento.profissional_saude

    def __str__(self):
        return f"Laudo para {self.paciente.nome} em {self.data_consulta}"

    class Meta:
        ordering = ['-data_laudo']
        verbose_name = 'Laudo'
        verbose_name_plural = 'Laudos'