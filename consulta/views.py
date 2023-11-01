from django.shortcuts import render, redirect
from .models import FilaEspera, Paciente
from datetime import date
from .models import FilaEspera
from django.shortcuts import render

def consultas_admissionais(request):
    # Lógica para as consultas admissionais para servidores externos
    return render(request, 'consultas/consultas_admissionais.html')

def adicionar_paciente_fila(request, paciente_id):
    paciente = Paciente.objects.get(pk=paciente_id)
    idade = paciente.idade()

    # Verifique se o paciente é idoso e defina a prioridade
    if idade >= 65:
        prioridade = True
    else:
        prioridade = False

    fila = FilaEspera(paciente=paciente, prioridade=prioridade)
    fila.save()
    return redirect('fila_espera')


def fila_espera(request):
    # Ordene a fila para que pacientes com prioridade apareçam primeiro
    pacientes_na_fila = FilaEspera.objects.order_by('-prioridade', 'data_chegada')
    return render(request, 'consultas/fila_espera.html', {'pacientes_na_fila': pacientes_na_fila})