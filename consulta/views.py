from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView

from consulta.models import FilaEspera, Paciente, Administrativo
from consulta.models import Agendamento, FilaEspera, Paciente, Profissionaldasaude
from datetime import date
from consulta.models import FilaEspera
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages





def home(request):
    return render(request, 'home.html')


def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'consultas/listagem_pacientes.html', {'pacientes': pacientes})

def listar_administrativo(request):
    administrativo = Administrativo.objects.all()
    return render(request, 'consultas/listagem_administrativo.html', {'administrativo': administrativo})


def listar_profissionaisdasaude(request):
    profissionaisdasaude = Profissionaldasaude.objects.all()
    return render(request, 'consultas/listagem_profissionaisdasaude.html', {'profissionaisdasaude': profissionaisdasaude})

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
    fields = ['nome', 'data_nascimento', 'email', 'rg', 'cpf', 'sexo', 'matricula', 'tipo_paciente',
              'cargo_funcao', 'ddd_telefone', 'uf', 'cep', 'cidade', 'bairro', 'numero', 'complemento']
    template_name = 'consultas/cadastro_paciente.html'
    success_url = reverse_lazy('pacienteListagem')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Paciente cadastrado com sucesso!')
        print("Paciente cadastrado com sucesso!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao cadastrar o paciente. Verifique os dados e tente novamente.')
        print("Erro ao cadastrar o paciente.")
        print(form.errors)  
        return super().form_invalid(form)


class AdministrativoCreate(CreateView):
    model = Administrativo
    fields = ['nome', 'data_nascimento','email','rg','cpf','sexo','matricula_siape','orgao','cargo_funcao','lotacao_de_exercicio','ddd_telefone','uf','cep','cidade','bairro','numero', 'complemento']
    template_name = 'consultas/cadastro_administrativo.html'
    success_url = reverse_lazy('administrativoListagem')
    
    
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Administrativo cadastrado com sucesso!')
        print("Administrativo cadastrado com sucesso!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao cadastrar o administrativo. Verifique os dados e tente novamente.')
        print("Erro ao cadastrar o administrativo.")
        print(form.errors)  
        return super().form_invalid(form)
    

    
class ProfissionaldasaudeCreate(CreateView):
    model = Profissionaldasaude
    fields = ['nome', 'data_nascimento','email','rg','cpf','sexo','identificacao_unica','area','formacao','conselho','registro','unidade_siass','ddd_telefone','uf','cep','cidade','bairro','numero', 'complemento']
    template_name = 'consultas/cadastro_profissionaldasaude.html'
    success_url = reverse_lazy('profissionaisdasaudeListagem')
    
    
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Profissional da saúde cadastrado com sucesso!')
        print("Profissional da saúde cadastrado com sucesso!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao cadastrar o profissional da saúde. Verifique os dados e tente novamente.')
        print("Erro ao cadastrar o profissional da saúde.")
        print(form.errors)  
        return super().form_invalid(form)



class AgendamentoCreate(CreateView):
    model = Agendamento
    fields = ['paciente','profissional_saude','data_agendamento','prioridade_atendimento']
    template_name = 'consultas/forms_agendamento.html'
    success_url = reverse_lazy('home')