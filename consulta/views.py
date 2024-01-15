from audioop import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from consulta.forms import AdministrativoForm, AgendamentoReagendarForm, AtendimentoForm, JustificativaCancelamentoForm, PacienteForm, PesquisaAgendamentoForm, ProfissionaldasaudeForm

from consulta.models import Atendimento, Paciente, Administrativo
from consulta.models import Agendamento, Paciente, Profissionaldasaude
from datetime import date
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
    form = PesquisaAgendamentoForm(request.GET)
    agendamentos = Agendamento.objects.all()

    if form.is_valid():
        cpf = form.cleaned_data.get('cpf')
        data_agendamento = form.cleaned_data.get('data_agendamento')

        if cpf:
            agendamentos = agendamentos.filter(paciente__cpf__icontains=cpf)

        if data_agendamento:
            agendamentos = agendamentos.filter(data_agendamento__date=data_agendamento)

    else:
        agendamentos = Agendamento.objects.all()

    # Ordenar os agendamentos pela data em ordem decrescente
    agendamentos = agendamentos.order_by('-data_agendamento')

    return render(request, 'consultas/listagem_agendamentos.html', {'form': form, 'agendamentos': agendamentos})


def agendamento_confirmar(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    agendamento.status_atendimento = 'confirmado'
    agendamento.save()
    messages.success(request, 'Agendamento confirmado com sucesso!')
    return redirect('agendamentoListagem')

def agendamento_ausente(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    agendamento.status_atendimento = 'ausente'
    agendamento.save()
    messages.success(request, 'Agendamento marcado como ausente com sucesso!')
    return redirect('agendamentoListagem')

def reagendar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)

    if request.method == 'POST':
        form = AgendamentoReagendarForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            
            # Após salvar o formulário, atualize o status para 'pendente'
            agendamento.status_atendimento = 'pendente'
            agendamento.save()

            messages.success(request, 'Agendamento reagendado com sucesso!')
            return redirect('agendamentoListagem')
    else:
        form = AgendamentoReagendarForm(instance=agendamento)

    return render(request, 'consultas/reagendar_agendamento.html', {'form': form, 'agendamento': agendamento})

def cancelar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, pk=agendamento_id)

    if request.method == 'POST':
        form = JustificativaCancelamentoForm(request.POST)
        if form.is_valid():
            agendamento.justificativa_cancelamento = form.cleaned_data['justificativa']
            agendamento.status_atendimento = 'cancelado'
            agendamento.save()

            # Retorna uma resposta JSON
            return JsonResponse({'success': True, 'message': 'Agendamento cancelado com sucesso.'})

    else:
        form = JustificativaCancelamentoForm()

    return render(request, 'consulta/cancelar_agendamento.html', {'form': form, 'agendamento': agendamento})


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
    success_url = reverse_lazy('agendamentoListagem')


class AtendimentoCreate(CreateView):
    model = Atendimento
    form_class = AtendimentoForm
    template_name = 'consultas/atendimento.html'

    def form_valid(self, form):
        # Antes de salvar o atendimento, obtenha o agendamento associado
        agendamento_id = self.kwargs['agendamento_id']
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        
        # Associe o agendamento ao atendimento
        form.instance.agendamento = agendamento

        response = super().form_valid(form)
        messages.success(self.request, 'Atendimento criado com sucesso!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar o atendimento. Verifique os dados e tente novamente.')
        return super().form_invalid(form)

    def get_success_url(self):
        # Após a criação do atendimento, redirecione para a tela de detalhes do agendamento
        agendamento_id = self.kwargs['agendamento_id']
        return reverse('agendamentoListagem', kwargs={'pk': agendamento_id})