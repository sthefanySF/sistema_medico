from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from consulta.forms import AdministrativoForm, PacienteForm, ProfissionaldasaudeForm

from consulta.models import FilaEspera, Paciente, Administrativo
from consulta.models import Agendamento, FilaEspera, Paciente, Profissionaldasaude
from datetime import date
from consulta.models import FilaEspera
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404






def home(request):
    return render(request, 'home.html')


def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'consultas/listagem_pacientes.html', {'pacientes': pacientes})


def paciente_editar(request, pk):
        paciente = get_object_or_404(Paciente, pk=pk)

        if request.method == 'POST':
            form = PacienteForm(request.POST, instance=paciente)
            if form.is_valid():
                form.save()
               
                return redirect('pacienteListagem')
        else:
            form = PacienteForm(instance=paciente)

        return render(request, 'consultas/editar_paciente.html', {'form': form, 'paciente': paciente})

def paciente_excluir(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        paciente.delete()
        
        return redirect('pacienteListagem')

    return render(request, 'consultas/excluir_paciente.html', {'paciente': paciente})

def listar_administrativo(request):
    administrativo = Administrativo.objects.all()
    return render(request, 'consultas/listagem_administrativo.html', {'administrativo': administrativo})


def administrativo_editar(request, pk):
        administrativo = get_object_or_404(Administrativo, pk=pk)

        if request.method == 'POST':
            form = AdministrativoForm(request.POST, instance=administrativo)
            if form.is_valid():
                form.save()
               
                return redirect('administrativoListagem')
        else:
            form = AdministrativoForm(instance=administrativo)

        return render(request, 'consultas/editar_administrativo.html', {'form': form, 'administrativo': administrativo})

def administrativo_excluir(request, pk):
    administrativo = get_object_or_404(Administrativo, pk=pk)

    if request.method == 'POST':
        administrativo.delete()
        
        return redirect('administrativoListagem')

    return render(request, 'consultas/excluir_administrativo.html', {'administrativo': administrativo})


def listar_profissionaldasaude(request):
    profissionaldasaude = Profissionaldasaude.objects.all()
    return render(request, 'consultas/listagem_profissionaldasaude.html', {'profissionaldasaude': profissionaldasaude})



def profissionaldasaude_editar(request, pk):
    profissionaldasaude = get_object_or_404(Profissionaldasaude, pk=pk)

    if request.method == 'POST':
        form = ProfissionaldasaudeForm(request.POST, instance=profissionaldasaude)
        if form.is_valid():
            form.save()
            return redirect('profissionaldasaudeListagem')
    else:
        form = ProfissionaldasaudeForm(instance=profissionaldasaude)

    return render(request, 'consultas/editar_proSaude.html', {'form': form, 'profissionaldasaude': profissionaldasaude})

def profissionaldasaude_excluir(request, pk):
    profissionaldasaude = get_object_or_404(Profissionaldasaude, pk=pk)

    if request.method == 'POST':
        profissionaldasaude.delete()
        
        return redirect('profissionaldasaudeListagem')

    return render(request, 'consultas/excluir_proSaude.html', {'profissionaldasaude': profissionaldasaude})


def listar_agendamentos(request):
    agendamentos = Agendamento.objects.all()
    return render(request, 'consultas/listagem_agendamentos.html', {'agendamentos': agendamentos})

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
    success_url = reverse_lazy('profissionaldasaudeListagem')
    
    
    
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