from django.db import models
from datetime import date


class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    email = models.EmailField()
    rg = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')])
    matricula = models.CharField(max_length=20)
    TIPO_PACIENTE_CHOICES = [
        ('Aluno', 'Aluno'),
        ('Servidor', 'Servidor'),
        ('Outro', 'Outro'),
    ]

    tipo_paciente = models.CharField(max_length=20, choices=TIPO_PACIENTE_CHOICES)
    cargo_funcao = models.CharField(max_length=50, default='', blank=True, null=True,)
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50, default='')
    uf = models.CharField(max_length=2)
    numero = models.CharField(max_length=10)
    ddd_telefone = models.CharField(max_length=3)
    complemento = models.CharField(max_length=100, blank=True, null=True, default='')  # Adicionando o valor padrão aqui



    def __str__(self):
        return self.nome

    
    
    def idade(self):
        today = date.today()
        age = today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return age 

class Administrativo(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    email = models.EmailField()
    rg = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')])
    cargo_funcao = models.CharField(max_length=50, default='')
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50, default='')
    uf = models.CharField(max_length=2)
    numero = models.CharField(max_length=10)
    ddd_telefone = models.CharField(max_length=3)
    complemento = models.CharField(max_length=100, blank=True, null=True, default='')
    orgao = models.CharField(max_length=50, default='')
    lotacao_de_exercicio = models.CharField(max_length=50, default='')
    matricula_siape = models.CharField(max_length=20)

    def __str__(self):
        return self.nome
    
    def idade(self):
        today = date.today()
        age = today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return age 
    
    
class Profissionaldasaude(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    email = models.EmailField()
    rg = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')]) #O parâmetro choices em um campo CharField ou IntegerField é usado para fornecer uma lista de escolhas para esse campo
    identificacao_unica = models.CharField(max_length=50, default='')
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50, default='')
    uf = models.CharField(max_length=2)
    numero = models.CharField(max_length=10)
    ddd_telefone = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True, default='') # blank=True, null=True é pra dizer que não é obrigatorio 
    area = models.CharField(max_length=50, default='')
    unidade_siass = models.CharField(max_length=50, default='')
    formacao = models.CharField(max_length=20)
    conselho = models.CharField(max_length=20)
    registro = models.CharField(max_length=20)
    

  

    def __str__(self):
        return self.nome
    
    def idade(self):
        today = date.today()
        age = today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return age 
    


class Agendamento(models.Model):
    status_atendimento = models.CharField(max_length=20, choices=[
        ('confirmado', 'Confirmado'),
        ('ausente', 'Ausente'),
        ('pendente', 'Pendente'),
    ], default='pendente')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE) #contem referncia do objeto Paciente
    #on_delete=models.CASCADE: Isso especifica o que acontecerá quando o objeto referenciado (Paciente) for excluído. 
    #Neste caso, CASCADE significa que, se um objeto Paciente for excluído, todos os objetos que têm uma referência a ele no campo paciente também serão excluídos.
    profissional_saude = models.ForeignKey(Profissionaldasaude, on_delete=models.CASCADE)  #contem referncia do objeto Profissionaldasaude
    data_agendamento = models.DateTimeField()
    prioridade_atendimento = models.BooleanField(default=False)
    justificativa_cancelamento = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Agendamento para {self.paciente.nome}"
    

class Atendimento(models.Model):
    agendamento = models.OneToOneField('Agendamento', on_delete=models.CASCADE)
    anamnese = models.TextField()
    exame_fisico = models.TextField()
    exames_complementares = models.TextField()
    pdf_exames = models.FileField(upload_to='exames_pdfs/', null=True, blank=True)
    diagnostico = models.TextField()
    conduta = models.TextField()

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



 