from django.db import models
from datetime import date


class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
   

    def idade(self):
        today = date.today()
        age = today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return age

    def __str__(self):
        return self.nome


class FilaEspera(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_chegada = models.DateTimeField(auto_now_add=True)
    prioridade = models.BooleanField(default=False)
    
    def __str__(self):
        return self.paciente.nome
