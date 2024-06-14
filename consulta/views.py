from audioop import reverse
from imaplib import _Authenticator
from multiprocessing import AuthenticationError
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import CreateView

# from consulta.forms import AdministrativoForm, AgendamentoForm, AgendamentoReagendarForm, AtendimentoForm,
# JustificativaCancelamentoForm, PacienteForm, PesquisaAgendamentoForm, ProfissionaldasaudeForm
import json
from django.http import JsonResponse
from consulta.forms import *
from django.views.decorators.http import require_POST
from consulta.models import Atendimento, Paciente, Administrativo
from consulta.models import Agendamento, Paciente, Profissionaldasaude, AtestadoMedico, ReceitaMedica
from datetime import date
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect


from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io

from django.template.response import TemplateResponse


# PARA ENVIAR E-MAIL
from django.core.mail import send_mail
from sistema_medico.settings import EMAIL_HOST_USER
from django.conf import settings

# para weasyprint e visualizar pdf
from django.http import FileResponse
from django.template.loader import get_template
from weasyprint import HTML

#filtrar pacientes
from django.core import serializers
from django.core.serializers import serialize

# permissoes de usuario
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    return render(request, 'home.html')

def prontuario_medico(request):
    return render(request, 'consultas/prontuario_medico.html')

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

@require_POST
def paciente_excluir(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    
    try:
        paciente.delete()
        messages.success(request, 'Paciente excluído')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('pacienteListagem')
    except Exception as e:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': str(e)})
        return render(request, 'consultas/excluir_paciente.html', {'paciente': paciente})


def is_administrativo(user):
    return user.groups.filter(name='administrativo').exists()

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


@require_POST
def administrativo_excluir(request, pk):
    administrativo = get_object_or_404(Administrativo, pk=pk)

    try:
        administrativo.delete()
        messages.success(request, 'Administrativo excluído')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('administrativoListagem')
    except Exception as e:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': str(e)})
        return render(request, 'consultas/excluir_administrativo.html', {'administrativo': administrativo})

# def administrativo_excluir(request, pk):
#     administrativo = get_object_or_404(Administrativo, pk=pk)

#     if request.method == 'POST':
#         administrativo.delete()
#         messages.error(request, 'Administrativo excluido')
        
#         return redirect('administrativoListagem')

#     return render(request, 'consultas/excluir_administrativo.html', {'administrativo': administrativo})

def is_profissionaldasaude(user):
    return user.groups.filter(name='profissionais de saude').exists()

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

@require_POST
def profissionaldasaude_excluir(request, pk):
    profissionaldasaude = get_object_or_404(Profissionaldasaude, pk=pk)

    try:
        profissionaldasaude.delete()
        messages.success(request, 'profissional da saude excluído')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('profissionaldasaudeListagem')
    except Exception as e:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': str(e)})
        return render(request, 'consultas/excluir_proSaude.html', {'profissionaldasaude': profissionaldasaude})


# def profissionaldasaude_excluir(request, pk):
#     profissionaldasaude = get_object_or_404(Profissionaldasaude, pk=pk)

#     if request.method == 'POST':
#         profissionaldasaude.delete()
#         messages.error(request, 'Profissional de saúde excluido')
        
#         return redirect('profissionaldasaudeListagem')

#     return render(request, 'consultas/excluir_proSaude.html', {'profissionaldasaude': profissionaldasaude})


def listar_agendamentos(request):
    # Obtém o valor do filtro do profissional de saúde a partir dos parâmetros da query
    profissional_id = request.GET.get('profissional_saude')

    # Busca todos os profissionais de saúde
    profissionais_saude = Profissionaldasaude.objects.all()

    # Filtra os agendamentos com base no profissional de saúde, se um profissional for selecionado
    if profissional_id and profissional_id != 'todos':
        agendamentos = Agendamento.objects.filter(profissional_saude_id=profissional_id)
    else:
        agendamentos = Agendamento.objects.all()

    # Atualiza os status dos agendamentos
    for agendamento in agendamentos:
        agendamento.atualizar_status()

    # Ordena os agendamentos pela data em ordem decrescente
    agendamentos = agendamentos.order_by('-data_agendamento')

    return render(request, 'consultas/listagem_agendamentos.html', {
        'agendamentos': agendamentos,
        'profissionais_saude': profissionais_saude
    })





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

    if agendamento.status_atendimento != 'pendente':
        messages.error(request, 'Este agendamento não pode ser reagendado porque não está pendente.')
        return redirect('agendamentoListagem')

    if request.method == 'POST':
        form = AgendamentoReagendarForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reagendado com sucesso!')
            return redirect('agendamentoListagem')
        else:
            messages.error(request, 'Informe uma data válida!')
    else:
        form = AgendamentoReagendarForm(instance=agendamento)

    return render(request, 'consultas/reagendar_agendamento.html', {'form': form, 'agendamento': agendamento})


@require_POST  # Certifica que a função aceita apenas requisições POST
def cancelar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, pk=agendamento_id)
    
    if agendamento.status_atendimento != 'pendente':
        return JsonResponse({'success': False, 'errors': 'Não é possível cancelar um agendamento que não está pendente.'})

    form = JustificativaCancelamentoForm(request.POST)

    if form.is_valid():
        justificativa = form.cleaned_data['justificativa']
        agendamento.justificativa_cancelamento = justificativa
        agendamento.status_atendimento = 'cancelado'
        agendamento.save()

        return JsonResponse({'success': True, 'message': 'Agendamento cancelado com sucesso.'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})
        

def visualizar_atendimento(request, atendimento_id):
    atendimento = get_object_or_404(Atendimento, id=atendimento_id)
    paciente = atendimento.agendamento.paciente
    try:
        atestado = AtestadoMedico.objects.get(agendamento=atendimento.agendamento)
    except AtestadoMedico.DoesNotExist:
        atestado = None
    return render(request, 'consultas/visualizar_atendimento.html', {
        'atendimento': atendimento,
        'paciente': paciente,
        'atestado': atestado
    })

def lista_atendimentos(request):
    atendimentos = Atendimento.objects.all()
    return render(request, 'consultas/lista_atendimentos.html', {'atendimentos': atendimentos})

# def user_login(request):
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


class PacienteCreate(CreateView):
    form_class = PacienteForm
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
    form_class = AdministrativoForm  # Substitua pelo seu formulário real
    template_name = 'consultas/cadastro_administrativo.html'
    success_url = reverse_lazy('administrativoListagem')


    def form_valid(self, form):
        # Salva o formulário mas não commit para customizações adicionais
        administrativo = form.save(commit=False)

        # Criação do usuário com base nos dados do formulário
        username = form.cleaned_data['cpf']
        email = form.cleaned_data['email']
        password = User.objects.make_random_password()  # Gera uma senha aleatória

        # Verifica se o nome de usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(self.request, 'CPF já cadastrado como nome de usuário. Por favor, utilize um CPF único.')
            return self.form_invalid(form)

        # Cria o usuário
        usuario = User.objects.create_user(username=username, email=email, password=password)

        # Associa o usuário criado ao campo 'usuario' do modelo Administrativo
        administrativo.usuario = usuario

        # Armazena a senha gerada no objeto Administrativo
        administrativo.senha_gerada = password

        # Salva o objeto Administrativo
        administrativo.save()

        # Adiciona o usuário ao grupo "administrativos"
        grupo_administrativo = Group.objects.get(name='administrativo')
        usuario.groups.add(grupo_administrativo)

        # Enviar e-mail de confirmação (opcional)
        assunto = 'Sistema Médico Pericial - UFAC - Confirmação de Cadastro'
        message = f'Olá {administrativo.nome}! Seu cadastro foi confirmado com sucesso! ' \
                  f'Seu login é o seu CPF. \n Por favor, clique no link abaixo para ' \
                  f'redefinir sua senha: \n www.google.com.br'
        try:
            send_mail(assunto, message, EMAIL_HOST_USER, [email])
            msg = 'Cadastrado com sucesso! Enviamos um e-mail de recuperação de senha.'
        except:
            msg = 'Cadastro realizado com sucesso!'

        messages.success(self.request, msg)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro! Verifique os campos preenchidos e tente novamente.')
        return super().form_invalid(form)

class ProfissionaldasaudeCreate(CreateView):
    model = Profissionaldasaude
    form_class = ProfissionaldasaudeForm
    template_name = 'consultas/cadastro_profissionaldasaude.html'
    success_url = reverse_lazy('profissionaldasaudeListagem')
    
    def form_valid(self, form):
        profissional = form.save(commit=False)
        
        username = form.cleaned_data['cpf']
        email = form.cleaned_data['email']
        password = User.objects.make_random_password()
        
        # Verifica se o nome de usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(self.request, 'CPF já cadastrado como nome de usuário. Por favor, utilize um CPF único.')
            return self.form_invalid(form)
        
                # Cria o usuário
        usuario = User.objects.create_user(username=username, email=email, password=password)

        # Associa o usuário criado ao campo 'usuario' do modelo Profissionaldasaude
        profissional.usuario = usuario

        # Armazena a senha gerada no objeto Profissionaldasaude
        profissional.senha_gerada = password
          
        profissional.save()
        
        # Adiciona o usuário ao grupo "Profissionais da saude"
        grupo_profissionaldasaude = Group.objects.get(name='profissionais de saude')
        usuario.groups.add(grupo_profissionaldasaude)

        # Enviar e-mail de confirmação
        assunto = 'Sistema Médico Pericial - UFAC - Confirmação de Cadastro'
        message = f'Olá {profissional.nome}! Seu cadastro foi confirmado com sucesso! ' \
                  f'Seu login é o seu CPF. \n Por favor, clique no link abaixo para ' \
                  f'redefinir sua senha: \n www.google.com.br'
        try:
            send_mail(assunto, message, EMAIL_HOST_USER, [email])
            msg = 'Cadastrado com sucesso! Enviamos um e-mail de recuperação de senha.'
        except:
            msg = 'Cadastro realizado com sucesso!'

        messages.success(self.request, msg)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Corrija o formulário!')
        return super().form_invalid(form)





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


@login_required
def criar_atendimento(request, agendamento_id):
    if request.method == 'POST':
        form = AtendimentoForm(request.POST)
        if form.is_valid():
            atendimento = form.save(commit=False)
            atendimento.agendamento_id = agendamento_id
            atendimento.save()
            messages.success(request, 'Atendimento criado com sucesso!')
            return redirect('listaAtendimentos')
    else:
        form = AtendimentoForm()

    return render(request, 'consultas/atendimento_form.html', {'form': form})

class AtendimentoCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Atendimento
    form_class = AtendimentoForm
    template_name = 'consultas/atendimento.html'
    
    def test_func(self):
        user = self.request.user
        return not is_administrativo(user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agendamento_id = self.kwargs['agendamento_id']
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        context['agendamento'] = agendamento
        context['atestado_medico_form'] = AtestadoMedicoForm(agendamento=agendamento)
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        agendamento_id = self.kwargs['agendamento_id']
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        
        atendimento_form = AtendimentoForm(request.POST, request.FILES)
        atestado_medico_form = AtestadoMedicoForm(request.POST, agendamento=agendamento)
        
        if atendimento_form.is_valid():
            return self.form_valid(atendimento_form, atestado_medico_form, agendamento)
        else:
            return self.form_invalid(atendimento_form, atestado_medico_form)

    def form_valid(self, atendimento_form, atestado_medico_form, agendamento):
        atendimento = atendimento_form.save(commit=False)
        atendimento.agendamento = agendamento
        atendimento.save()

        agendamento.status_atendimento = 'atendido'
        agendamento.save()

        # Verifica se os campos do atestado médico estão preenchidos antes de salvar
        if atestado_medico_form.is_valid():
            dias_afastamento = atestado_medico_form.cleaned_data.get('dias_afastamento')
            cid = atestado_medico_form.cleaned_data.get('cid')
            if dias_afastamento or cid:
                atestado_medico = atestado_medico_form.save(commit=False)
                atestado_medico.agendamento = agendamento
                atestado_medico.save()

        return redirect('confirmar_atendimento', agendamento_id=agendamento.id)

    def form_invalid(self, atendimento_form, atestado_medico_form):
        context = self.get_context_data()
        context['form'] = atendimento_form
        context['atestado_medico_form'] = atestado_medico_form
        return self.render_to_response(context)


    # def test_func(self):
    #     return is_profissionaldasaude(self.request.user)
    
    # permite todos acessarem
    # def test_func(self):
    #     return True


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


def visualizar_pdf_exames(request, atendimento_id):
    atendimento = get_object_or_404(Atendimento, id=atendimento_id)

    # Verifica se o atendimento possui um PDF de exames
    if atendimento.pdf_exames:
        pdf_file_path = atendimento.pdf_exames.path
        with open(pdf_file_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'filename=pdf_exames_atendimento_{atendimento_id}.pdf'
            return response
    else:
        # Caso não tenha PDF de exames, você pode retornar uma mensagem de erro ou redirecionar para outra página
        return HttpResponse("PDF de exames não encontrado.")
  
    
def visualizar_comprovante_atendimento(request, atendimento_id):
    atendimento = get_object_or_404(Atendimento, id=atendimento_id)

    # Renderiza o template para HTML
    html_content = render_to_string('consultas/comprovantePdf_atendimento.html', {'atendimento': atendimento})
    
    # Converte HTML para PDF
    pdf_file = io.BytesIO()
    pisa.CreatePDF(html_content, dest=pdf_file)
    
    # Configura o conteúdo do PDF para visualização
    pdf_file.seek(0)
    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'filename=comprovante_atendimento_{atendimento_id}.pdf'
    
    return response

# def filtrar_prontuarios(request):
#     paciente_id = request.GET.get('paciente_id')
#     medicos_ids = request.GET.getlist('medicos')

#     paciente = get_object_or_404(Paciente, pk=paciente_id)
#     ids_agendamentos = paciente.agendamento_set.all().values_list('id', flat=True)

#     atendimentos = Atendimento.objects.filter(agendamento__id__in=ids_agendamentos, agendamento__profissional_saude__id__in=medicos_ids)

#     # Serializa os objetos com representação natural de chaves estrangeiras
#     data = serialize('json', atendimentos, use_natural_foreign_keys=True, fields=('profissional_saude', 'paciente', 'data_atendimento', 'anamnese', 'exame_fisico', 'exames_complementares', 'diagnostico', 'conduta'))
#     return HttpResponse(data, content_type='application/json')

def prontuario_medico(request, paciente_id):
    paciente = Paciente.objects.get(pk=paciente_id)
    atendimentos = Atendimento.objects.filter(agendamento__paciente=paciente)
    profissionais_saude = Profissionaldasaude.objects.all()  # Obter todos os médicos
    return render(request, 'consultas/prontuario_medico.html', {'paciente': paciente, 'atendimentos': atendimentos, 'profissionais_saude': profissionais_saude})


def filtrar_prontuarios(request):
    paciente_id = request.GET.get('paciente_id')
    medicos_ids = request.GET.getlist('medicos')

    paciente = get_object_or_404(Paciente, pk=paciente_id)
    ids_agendamentos = paciente.agendamento_set.all().values_list('id', flat=True)

    if not medicos_ids:  # Se nenhum médico foi selecionado, retornar todos os atendimentos
        atendimentos = Atendimento.objects.filter(agendamento__paciente=paciente)
    else:
        atendimentos = Atendimento.objects.filter(agendamento__id__in=ids_agendamentos, agendamento__profissional_saude__id__in=medicos_ids)

    # Construindo a lista de dicionários para cada atendimento
    atendimentos_list = []
    for atendimento in atendimentos:
        atendimento_dict = {
            'profissional_saude': atendimento.agendamento.profissional_saude.nome,
            'area': atendimento.agendamento.profissional_saude.area,
            'paciente': atendimento.agendamento.paciente.nome,
            'data_atendimento': atendimento.data_atendimento.strftime('%d-%m-%Y'),  # Formatar a data para string
            'anamnese': atendimento.anamnese,
            'exame_fisico': atendimento.exame_fisico,
            'exames_complementares': atendimento.exames_complementares,
            'diagnostico': atendimento.diagnostico,
            'conduta': atendimento.conduta
        }
        atendimentos_list.append(atendimento_dict)

    # Convertendo a lista de dicionários para JSON
    data = json.dumps(atendimentos_list)

    return HttpResponse(data, content_type='application/json')

def pdf_prontuario_medico(request, paciente_id):
    paciente = Paciente.objects.get(pk=paciente_id)
    medicos_ids = request.GET.get('medicos')

    if medicos_ids:
        medicos_ids = [int(id) for id in medicos_ids.split(",")]

        ids_agendamentos = paciente.agendamento_set.filter(profissional_saude__id__in=medicos_ids).values_list('id', flat=True)
        atendimentos = Atendimento.objects.filter(agendamento__id__in=ids_agendamentos)
    else:
        # Se nenhum médico for selecionado, obter todos os atendimentos do paciente
        atendimentos = Atendimento.objects.filter(agendamento__paciente=paciente)
        
    context = {
        'paciente': paciente,
        'atendimentos': atendimentos,
        'medicos_ids': medicos_ids,
    }

    html = render_to_string('pdfs/pdf_prontuario_medico.html', context)

    # Use WeasyPrint para transformar o HTML em PDF.
    pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="prontuario_medico.pdf"'
    return response

class AtestadoMedicoCreate(CreateView):
    model = AtestadoMedico
    form_class = AtestadoMedicoForm
    template_name = 'consultas/atestado_medico.html'

    # Método chamado quando o formulário é válido
    def form_valid(self, form):
        agendamento_id = self.kwargs['agendamento_id']
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        form.instance.agendamento = agendamento
        return super().form_valid(form)

    # Método para passar argumentos extras para o formulário
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        agendamento_id = self.kwargs['agendamento_id']
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        kwargs['agendamento'] = agendamento
        return kwargs

    # Método para adicionar dados adicionais ao contexto do template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agendamento_id = self.kwargs['agendamento_id']
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        context['paciente'] = agendamento.paciente.nome
        context['profissional'] = agendamento.profissional_saude.nome
        context['data_agendamento'] = agendamento.data_agendamento
        context['data_criacao'] = timezone.now()
        return context

    # Método para obter a URL de redirecionamento após o sucesso do envio do formulário
    def get_success_url(self):
        agendamento_id = self.kwargs['agendamento_id']
        return reverse('atestado_medico_create', kwargs={'agendamento_id': agendamento_id})


class CriarReceitaMedicaView(CreateView):
    def get(self, request, agendamento_id):
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        form = ReceitaMedicaForm(initial={'paciente_nome': agendamento.paciente.nome})  # Inicializa o formulário com o nome do paciente
        return render(request, 'consultas/criar_receita_medica.html', {'form': form, 'agendamento': agendamento})

    def post(self, request, agendamento_id):
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        form = ReceitaMedicaForm(request.POST)
        if form.is_valid():
            receita = form.save(commit=False)
            receita.agendamento = agendamento
            receita.save()
            
        return render(request, 'consultas/criar_receita_medica.html', {'form': form, 'agendamento': agendamento})

class ListarReceitasMedicasView(CreateView):
    def get(self, request, agendamento_id):
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        receitas = ReceitaMedica.objects.filter(agendamento=agendamento)
        return render(request, 'listar_receitas_medicas.html', {'receitas': receitas, 'agendamento': agendamento})