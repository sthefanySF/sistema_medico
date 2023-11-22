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
    tipo_paciente = models.CharField(max_length=20)
    cargo_funcao = models.CharField(max_length=50, default='')
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50, default='nome')
    uf = models.CharField(max_length=2)
    numero = models.CharField(max_length=10)
    ddd_telefone = models.CharField(max_length=3)
    complemento = models.CharField(max_length=100, blank=True, null=True, default='')  # Adicionando o valor padrão aqui



    def _str_(self):
        return self.nome
    
    
    def idade(self):
        today = date.today()
        age = today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return age 


class FilaEspera(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_chegada = models.DateTimeField(auto_now_add=True)
    prioridade = models.BooleanField(default=False)
    
    def _str_(self):
        return self.paciente.nome