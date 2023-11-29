from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView

from consulta.models import FilaEspera, Paciente, Administrativo
from consulta.models import Agendamento, FilaEspera, Paciente, Profissionaldasaude
from datetime import date
from consulta.models import FilaEspera
from django.shortcuts import render
from django.urls import reverse_lazy



def home(request):
    return render(request, 'home.html')


def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'consultas/listagem_pacientes.html', {'pacientes': pacientes})


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



class PacienteCreate(CreateView):
    model = Paciente
    fields = ['nome', 'data_nascimento','email','rg','cpf','sexo','matricula','tipo_paciente','cargo_funcao','ddd_telefone','uf','cep','cidade','bairro','numero', 'complemento']
    template_name = 'consultas/cadastro_paciente.html'
    success_url = reverse_lazy('home')

class AdministrativoCreate(CreateView):
    model = Administrativo
    fields = ['nome', 'data_nascimento','email','rg','cpf','sexo','matricula_siape','orgao','cargo_funcao','lotacao_de_exercicio','ddd_telefone','uf','cep','cidade','bairro','numero', 'complemento']
    template_name = 'consultas/cadastro_administrativo.html'
    success_url = reverse_lazy('home')
    
class ProfissionaldasaudeCreate(CreateView):
    model = Profissionaldasaude
    fields = ['nome', 'data_nascimento','email','rg','cpf','sexo','identificacao_unica','area','formacao','conselho','registro','unidade_siass','ddd_telefone','uf','cep','cidade','bairro','numero', 'complemento']
    template_name = 'consultas/cadastro_profissionaldasaude.html'
    success_url = reverse_lazy('home')



class AgendamentoCreate(CreateView):
    model = Agendamento
    fields = ['paciente','profissional_saude','data_agendamento','prioridade_atendimento']
    template_name = 'consultas/forms_agendamento.html'
    success_url = reverse_lazy('home')