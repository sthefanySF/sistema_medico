from audioop import reverse
from imaplib import _Authenticator
from multiprocessing import AuthenticationError
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import CreateView

# from consulta.forms import AdministrativoForm, AgendamentoForm, AgendamentoReagendarForm, AtendimentoForm,
# JustificativaCancelamentoForm, PacienteForm, PesquisaAgendamentoForm, ProfissionaldasaudeForm
from consulta.forms import *

from consulta.models import Atendimento, Paciente, Administrativo
from consulta.models import Agendamento, Paciente, Profissionaldasaude
from datetime import date
from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io

from django.template.response import TemplateResponse


def home(request):
    return render(request, 'home.html')


def logar(request):
    if request.user.is_authenticated:
        return redirect('agendamentoListagem')
    if request.method == 'POST':
        # form = AuthenticationForm(request, request.POST)
        usuario = request.POST['usuario']
        usuario = usuario.replace('.', '').replace('-', '')
        senha = request.POST['senha']
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('agendamentoListagem')
            else:
                messages.error(request, 'Usuário inativo. Entre em contato com a administração do sistema.')
        else:
            messages.error(request, 'Usuário ou senha inválidos! Tente novamente.')
    return render(request, 'consultas/login.html', locals())


@login_required()
def sair(request):
    logout(request)
    return redirect('home')

# def login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'consultas/login.html', {'form': form})
# #



@login_required
def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'consultas/listagem_pacientes.html', {'pacientes': pacientes})

@login_required
def paciente_editar(request, pk):
        paciente = get_object_or_404(Paciente, pk=pk)

        if request.method == 'POST':
            form = PacienteForm(request.POST, instance=paciente)
            if form.is_valid():
                form.save()
                messages.success(request, 'Cadastrado atualizado!')
               
                return redirect('pacienteListagem')
        else:
            form = PacienteForm(instance=paciente)

        return render(request, 'consultas/editar_paciente.html', {'form': form, 'paciente': paciente})

def paciente_excluir(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)

    if request.method == 'POST':
        paciente.delete()
        messages.error(request, 'Paciente excluido')
        
        return redirect('pacienteListagem')

    return render(request, 'consultas/excluir_paciente.html', {'paciente': paciente})


@login_required
def listar_administrativo(request):
    administrativo = Administrativo.objects.all()
    return render(request, 'consultas/listagem_administrativo.html', {'administrativo': administrativo})


@login_required
def administrativo_editar(request, pk):
        administrativo = get_object_or_404(Administrativo, pk=pk)

        if request.method == 'POST':
            form = AdministrativoForm(request.POST, instance=administrativo)
            if form.is_valid():
                form.save()
                messages.success(request, 'Cadastrado atualizado!')
               
                return redirect('administrativoListagem')
        else:
            form = AdministrativoForm(instance=administrativo)

        return render(request, 'consultas/editar_administrativo.html', {'form': form, 'administrativo': administrativo})

def administrativo_excluir(request, pk):
    administrativo = get_object_or_404(Administrativo, pk=pk)

    if request.method == 'POST':
        administrativo.delete()
        messages.error(request, 'Administrativo excluido')
        
        return redirect('administrativoListagem')

    return render(request, 'consultas/excluir_administrativo.html', {'administrativo': administrativo})

@login_required
def listar_profissionaldasaude(request):
    profissionaldasaude = Profissionaldasaude.objects.all()
    return render(request, 'consultas/listagem_profissionaldasaude.html', {'profissionaldasaude': profissionaldasaude})


@login_required
def profissionaldasaude_editar(request, pk):
    profissionaldasaude = get_object_or_404(Profissionaldasaude, pk=pk)

    if request.method == 'POST':
        form = ProfissionaldasaudeForm(request.POST, instance=profissionaldasaude)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro atualizado.')
            return redirect('profissionaldasaudeListagem')
    else:
        form = ProfissionaldasaudeForm(instance=profissionaldasaude)

    return render(request, 'consultas/editar_proSaude.html', {'form': form, 'profissionaldasaude': profissionaldasaude})

def profissionaldasaude_excluir(request, pk):
    profissionaldasaude = get_object_or_404(Profissionaldasaude, pk=pk)

    if request.method == 'POST':
        profissionaldasaude.delete()
        messages.error(request, 'Profissional de saúde excluido')
        
        return redirect('profissionaldasaudeListagem')

    return render(request, 'consultas/excluir_proSaude.html', {'profissionaldasaude': profissionaldasaude})


def listar_agendamentos(request):
    form = PesquisaAgendamentoForm(request.GET)
    agendamentos = Agendamento.objects.all()
    profissionais_saude = Profissionaldasaude.objects.all()

    profissional_id = request.GET.get('profissional_saude')

    if form.is_valid() and profissional_id and profissional_id != 'todos':
        cpf = form.cleaned_data.get('cpf')
        data_agendamento = form.cleaned_data.get('data_agendamento')

        if cpf:
            agendamentos = agendamentos.filter(paciente__cpf__icontains=cpf)

        if data_agendamento:
            agendamentos = agendamentos.filter(data_agendamento__date=data_agendamento)

        agendamentos = agendamentos.filter(profissional_saude_id=profissional_id)

    # Ordenar os agendamentos pela data em ordem decrescente
    agendamentos = agendamentos.order_by('-data_agendamento')

    return render(request, 'consultas/listagem_agendamentos.html', {'form': form, 'agendamentos': agendamentos, 'profissionais_saude': profissionais_saude})




def agendamento_confirmar(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    agendamento.status_atendimento = 'confirmado'
    agendamento.save()
    messages.success(request, 'Agendamento confirmado!')
    return redirect('agendamentoListagem')

def agendamento_ausente(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    agendamento.status_atendimento = 'ausente'
    agendamento.save()
    messages.warning(request, 'Agendamento definido como ausente!')
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

            messages.warning(request, 'Reagendado com sucesso!')
            return redirect('agendamentoListagem')
        else:
            messages.error(request, 'Informe uma data válida!')
            # Solicita uma data válida  para o formato da data.

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

    return render(request, 'consultas/cancelar_agendamento.html', {'form': form, 'agendamento': agendamento})


def visualizar_atendimento(request, atendimento_id):
    atendimento = get_object_or_404(Atendimento, id=atendimento_id)
    return render(request, 'consultas/visualizar_atendimento.html', {'atendimento': atendimento})

def lista_atendimentos(request):
    atendimentos = Atendimento.objects.all()
    return render(request, 'consultas/lista_atendimentos.html', {'atendimentos': atendimentos})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'consultas/login.html', {'form': form})


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
        messages.success(self.request, 'Cadastrado com sucesso! Um email foi enviado para definir a senha.')
        response = super().form_valid(form)
        
        #usuário com base nos dados do formulário
        username = form.cleaned_data['cpf']  
        email = form.cleaned_data['email']
        password = User.objects.make_random_password()  # Gera uma senha aleatória
        #usuário associado ao Administrativo
        usuario = User.objects.create_user(username=username, email=email, password=password)
        #Associa o usuário criado ao campo 'usuario' do modelo Administrativo
        self.object.usuario = usuario
        #Armazena a senha no objeto Administrativo
        self.object.senha_gerada = password
        usuario.save()
        self.object.save()

        
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Erro! Verifique os campos preenchidos e tente novamente.')
        return super().form_invalid(form)


# CÓDIGO DA RAQUEL
def ProfissionaldasaudeCreate(request):

    if request.method == 'POST':
        formps = ProfissionaldasaudeForm(request.POST)
        # formu = UserForm
        # if formps.is_valid() and formu.is_valid():
        if formps.is_valid():
            ps = formps.save(commit=False)
            ps.save()
            # fu = formu.save(commit=False)
            messages.success(request, 'Cadastrado com sucesso!')
            return redirect(reverse_lazy('profissionaldasaudeListagem'))
        else:
            messages.error(request, 'Corrija o formulário!')

    else:
        formps = ProfissionaldasaudeForm()

    return TemplateResponse(request, 'consultas/cadastro_profissionaldasaude.html', locals())





# class ProfissionaldasaudeCreate(CreateView):
#     model = Profissionaldasaude
#     fields = ['nome', 'data_nascimento','email','rg','cpf','sexo','identificacao_unica','area','formacao','conselho','registro','unidade_siass','ddd_telefone','uf','cep','cidade','bairro','numero', 'complemento']
#     template_name = 'consultas/cadastro_profissionaldasaude.html'
#     success_url = reverse_lazy('profissionaldasaudeListagem')
#
#
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(self.request, 'Profissional da saúde cadastrado com sucesso!')
#         print("Profissional da saúde cadastrado com sucesso!")
#         return response
#
#     def form_invalid(self, form):
#         messages.error(self.request, 'Erro ao cadastrar o profissional da saúde. Verifique os dados e tente novamente.')
#         print("Erro ao cadastrar o profissional da saúde.")
#         print(form.errors)
#         return super().form_invalid(form)



class AgendamentoCreate(CreateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'consultas/forms_agendamento.html'
    success_url = reverse_lazy('agendamentoListagem')

    def form_valid(self, form):
        # Criar o objeto apenas se o formulário for válido
        response = super().form_valid(form)

        # Redireciona para a tela de confirmação
        return redirect('confirmAgendamento', pk=self.object.pk)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao realizar o agendamento. Verifique os dados e tente novamente.')
        print("Erro ao realizar o agendamento.")
        print(form.errors)  
        
        # Renderizar o template novamente com o formulário inválido
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context
    

    def generate_pdf(self, agendamento):
        html_content = render_to_string('consultas/comprovantePdf_agendamento.html', {'agendamento': agendamento})

        pdf_file = io.BytesIO()
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

        if pisa_status.err:
            raise Exception("Erro ao gerar PDF.")

        pdf_file.seek(0)
        return pdf_file
    
def confirm_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    return render(request, 'consultas/confirm_agendamento.html', {'agendamento': agendamento})

def download_comprovante(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)

    html_content = render_to_string('consultas/comprovantePdf_agendamento.html', {'agendamento': agendamento})

    pdf_file = io.BytesIO()
    pisa.CreatePDF(html_content, dest=pdf_file)

    pdf_file.seek(0)

    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Comprovante_Agendamento_{agendamento.id}.pdf'

    return response


class AtendimentoCreate(CreateView):
    model = Atendimento
    form_class = AtendimentoForm
    template_name = 'consultas/atendimento.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agendamento_id = self.kwargs['agendamento_id']
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        context['agendamento'] = agendamento
        return context

    def form_valid(self, form):
        agendamento_id = self.kwargs['agendamento_id']
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        form.instance.agendamento = agendamento
        
        # Salva o atendimento
        atendimento = form.save()

        # Redireciona para a tela de confirmação de atendimento com o ID do Atendimento
        return redirect('confirmar_atendimento', agendamento_id=agendamento_id)

def confirmar_atendimento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    atendimento = agendamento.atendimento
    return render(request, 'consultas/confirmar_atendimento.html', {'atendimento': atendimento})


def download_comprovante_atendimento(request, atendimento_id):
    atendimento = get_object_or_404(Atendimento, id=atendimento_id)

    # Renderiza o template para HTML
    html_content = render_to_string('consultas/comprovantePdf_atendimento.html', {'atendimento': atendimento})
    
    # Converte HTML para PDF
    pdf_file = io.BytesIO()
    pisa.CreatePDF(html_content, dest=pdf_file)
    
    # Configura o conteúdo do PDF para download
    pdf_file.seek(0)
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=comprovante_atendimento_{atendimento_id}.pdf'
    
    return response