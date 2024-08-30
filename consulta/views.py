import tempfile
import os
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
from consulta.models import ArquivoPaciente, Atendimento, Paciente, Administrativo
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
from weasyprint import HTML, CSS


#filtrar pacientes
from django.core import serializers
from django.core.serializers import serialize

# permissoes de usuario
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin


from django.shortcuts import render
# from django.core.files.storage import FileSystemStorage


def home(request):
    return render(request, 'home.html')

def prontuario_medico(request):
    return render(request, 'consultas/prontuario_medico.html')

@login_required
def linha_usuario(request): #mostrar o usuario logado
    user = request.user
    context = {
        'user': user,
    }

    profissional_saude = Profissionaldasaude.objects.filter(usuario=user).first()
    context['profissional_saude'] = profissional_saude

    administrativo = Administrativo.objects.filter(usuario=user).first()
    context['administrativo'] = administrativo

    print("Context:", context)  # Debugging

    return render(request, 'linha_usuario.html', context)

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
    return redirect('login')

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
    pacientes = Paciente.objects.all().order_by('nome')
    form = PacienteForm()
    return render(request, 'consultas/listagem_pacientes.html', {'pacientes': pacientes, 'form': form})

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

#modal
@login_required
def editar_paciente(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("Recebendo POST request via AJAX")
        id = request.POST.get('id')
        print(f"ID recebido: {id}")
        paciente = get_object_or_404(Paciente, id=id)
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            print("Formulário válido e salvo com sucesso.")
            return JsonResponse({'success': True})
        else:
            print(f"Formulário inválido: {form.errors}")
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        print("Recebendo GET request")
        id = request.GET.get('id')
        paciente = get_object_or_404(Paciente, id=id)
        form = PacienteForm(instance=paciente)
        context = {
            'form': form,
            'paciente': paciente
        }
        return render(request, 'consultas/editar_paciente.html', context)

def is_administrativo(user):
    return user.groups.filter(name='administrativo').exists()

@login_required
def listar_administrativo(request):
    administrativo = Administrativo.objects.all()
    form = AdministrativoForm()
    return render(request, 'consultas/listagem_administrativo.html', {'administrativo': administrativo, 'form': form})

# modal
@login_required
def editar_administrativo(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("Recebendo POST request via AJAX")
        id = request.POST.get('id')
        print(f"ID recebido: {id}")
        administrativo = get_object_or_404(Administrativo, id=id)
        form = AdministrativoForm(request.POST, instance=administrativo)
        if form.is_valid():
            form.save()
            print("Formulário válido e salvo com sucesso.")
            return JsonResponse({'success': True})
        else:
            print(f"Formulário inválido: {form.errors}")
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        print("Recebendo GET request")
        id = request.GET.get('id')
        administrativo = get_object_or_404(Administrativo, id=id)
        form = AdministrativoForm(instance=administrativo)
        context = {
            'form': form,
            'administrativo': administrativo
        }
        return render(request, 'consultas/editar_administrativo.html', context)




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
    usuario = administrativo.usuario

    try:
        administrativo.delete()
        if usuario:
            usuario.delete()  # Exclui o usuário relacionado, se existir
        messages.success(request, 'Administrativo e usuário excluídos com sucesso')
        
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
    form = ProfissionaldasaudeForm()
    return render(request, 'consultas/listagem_profissionaldasaude.html', {'profissionaldasaude': profissionaldasaude, 'form': form})

#modal
@login_required
def editar_profissionaldasaude(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("Recebendo POST request via AJAX")
        id = request.POST.get('id')
        print(f"ID recebido: {id}")
        profissionaldasaude = get_object_or_404(Profissionaldasaude, id=id)
        form = ProfissionaldasaudeForm(request.POST, instance=profissionaldasaude)
        if form.is_valid():
            form.save()
            print("Formulário válido e salvo com sucesso.")
            return JsonResponse({'success': True})
        else:
            print(f"Formulário inválido: {form.errors}")
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        print("Recebendo GET request")
        id = request.GET.get('id')
        profissionaldasaude = get_object_or_404(Profissionaldasaude, id=id)
        form = ProfissionaldasaudeForm(instance=profissionaldasaude)
        context = {
            'form': form,
            'profissionaldasaude': profissionaldasaude
        }
        return render(request, 'consultas/editar_profissionaldasaude.html', context)


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
    usuario = profissionaldasaude.usuario

    try:
        profissionaldasaude.delete()
        if usuario:
            usuario.delete()
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
    profissional_id = request.GET.get('profissional_saude')
    form = AgendamentoForm()
    profissionais_saude = Profissionaldasaude.objects.all()

    if profissional_id and profissional_id != 'todos':
        agendamentos = Agendamento.objects.filter(profissional_saude_id=profissional_id)
    else:
        agendamentos = Agendamento.objects.all()

    for agendamento in agendamentos:
        if agendamento.status_atendimento != 'atendido':
            agendamento.atualizar_status()

    agendamentos = agendamentos.order_by('-data_agendamento')

    return render(request, 'consultas/listagem_agendamentos.html', {
        'agendamentos': agendamentos,
        'profissionais_saude': profissionais_saude,
        'form': form
    })
    
def confirm_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    return render(request, 'consultas/confirm_agendamento.html', {'agendamento': agendamento})


def agendamento_confirmar(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)

    # Verifica se data_agendamento não é None
    if agendamento.data_agendamento is None:
        messages.error(request, 'Data de agendamento não definida.')
        return redirect('agendamentoListagem')

    # Verifica se a data do agendamento é igual à data atual
    if agendamento.data_agendamento != timezone.now().date():
        messages.error(request, 'O agendamento só pode ser confirmado na data prevista.')
        return redirect('agendamentoListagem')

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
        return JsonResponse({'success': False, 'errors': 'Este agendamento não pode ser reagendado porque não está pendente.'})

    if request.method == 'POST':
        form = AgendamentoReagendarForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        return JsonResponse({'success': False, 'errors': 'Método de requisição inválido.'})


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

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})
        

def visualizar_atendimento(request, atendimento_id):
    atendimento = get_object_or_404(Atendimento, id=atendimento_id)
    paciente = atendimento.agendamento.paciente
    
    # Buscar o atestado médico
    try:
        atestado = AtestadoMedico.objects.get(agendamento=atendimento.agendamento)
        if atestado.dias_afastamento == 0 and atestado.cid == 'N/A':
            atestado = None
    except AtestadoMedico.DoesNotExist:
        atestado = None

    # Buscar as receitas médicas
    receita_simples = ReceitaMedica.objects.filter(agendamento=atendimento.agendamento, tipo='simples').first()
    receita_controle_especial = ReceitaMedica.objects.filter(agendamento=atendimento.agendamento, tipo='controle_especial').first()

    # Buscar os laudos médicos
    laudos = Laudo.objects.filter(agendamento=atendimento.agendamento).order_by('-data_laudo')

    # Multiplos Arquivos
    if request.method == 'POST' and 'file_field' in request.FILES:
        form = MultipleFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file_field')
            for f in files:
                ArquivoPaciente.objects.create(paciente=paciente, arquivo=f)

            messages.success(request, 'Enviado com sucesso!')
            return redirect('visualizarAtendimento', atendimento_id=atendimento_id)
    else:
        form = MultipleFileForm()

    arquivos = ArquivoPaciente.objects.filter(paciente=paciente).order_by('-data_envio')
    # Fim

    return render(request, 'consultas/visualizar_atendimento.html', {
        'atendimento': atendimento,
        'paciente': paciente,
        'atestado': atestado,
        'receita_simples': receita_simples,
        'receita_controle_especial': receita_controle_especial,
        'laudos': laudos,
        'arquivos': arquivos,
        'form': form,
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

    def is_ajax(self):
        return self.request.headers.get('x-requested-with') == 'XMLHttpRequest'

    def form_valid(self, form):
        cpf = form.cleaned_data['cpf']
        if Paciente.objects.filter(cpf=cpf).exists():
            if self.is_ajax():
                return JsonResponse({'success': False, 'errors': {'cpf': 'CPF já cadastrado. Por favor, utilize um CPF único.'}})
            messages.error(self.request, 'CPF já cadastrado. Por favor, utilize um CPF único.')
            return self.form_invalid(form)

        response = super().form_valid(form)
        messages.success(self.request, 'Paciente cadastrado com sucesso!')
        if self.is_ajax():
            return JsonResponse({'success': True, 'message': 'Paciente cadastrado com sucesso!'})
        return response

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors})
        messages.error(self.request, 'Erro ao cadastrar o paciente. Verifique os dados e tente novamente.')
        return super().form_invalid(form) 

class AdministrativoCreate(CreateView):
    model = Administrativo
    form_class = AdministrativoForm
    template_name = 'consultas/cadastro_administrativo.html'
    success_url = reverse_lazy('administrativoListagem')

    def is_ajax(self):
        return self.request.headers.get('x-requested-with') == 'XMLHttpRequest'

    def form_valid(self, form):
        administrativo = form.save(commit=False)

        username = form.cleaned_data['cpf']
        email = form.cleaned_data['email']
        password = User.objects.make_random_password()

        if User.objects.filter(username=username).exists():
            if self.is_ajax():
                return JsonResponse({'success': False, 'errors': {'username': 'CPF já cadastrado como nome de usuário. Por favor, utilize um CPF único.'}})
            messages.error(self.request, 'CPF já cadastrado como nome de usuário. Por favor, utilize um CPF único.')
            return self.form_invalid(form)

        usuario = User.objects.create_user(username=username, email=email, password=password)

        administrativo.usuario = usuario
        administrativo.senha_gerada = password
        administrativo.save()

        grupo_administrativo = Group.objects.get(name='administrativo')
        usuario.groups.add(grupo_administrativo)

        assunto = 'Sistema Médico Pericial - UFAC - Confirmação de Cadastro'
        message = f'Olá {administrativo.nome}! Seu cadastro foi confirmado com sucesso! ' \
                  f'Seu login é o seu CPF. \n Por favor, clique no link abaixo para ' \
                  f'redefinir sua senha: \n www.google.com.br'
        try:
            send_mail(assunto, message, EMAIL_HOST_USER, [email])
            msg = 'Cadastrado com sucesso! Enviamos um e-mail de recuperação de senha.'
        except:
            msg = 'Cadastro realizado com sucesso!'

        if self.is_ajax():
            return JsonResponse({'success': True, 'message': msg})

        messages.success(self.request, msg)
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors})
        messages.error(self.request, 'Erro! Verifique os campos preenchidos e tente novamente.')
        return super().form_invalid(form)

class ProfissionaldasaudeCreate(CreateView):
    model = Profissionaldasaude
    form_class = ProfissionaldasaudeForm
    # template_name = 'consultas/cadastro_profissionaldasaude.html'
    success_url = reverse_lazy('profissionaldasaudeListagem')
    
    def is_ajax(self):
        return self.request.headers.get('x-requested-with') == 'XMLHttpRequest'

    def form_valid(self, form):
        profissional = form.save(commit=False)

        username = form.cleaned_data['cpf']
        email = form.cleaned_data['email']
        password = User.objects.make_random_password()

        if User.objects.filter(username=username).exists():
            if self.is_ajax():
                return JsonResponse({'success': False, 'errors': {'username': 'CPF já cadastrado como nome de usuário. Por favor, utilize um CPF único.'}})
            messages.error(self.request, 'CPF já cadastrado como nome de usuário. Por favor, utilize um CPF único.')
            return self.form_invalid(form)

        usuario = User.objects.create_user(username=username, email=email, password=password)

        profissional.usuario = usuario
        profissional.senha_gerada = password
        profissional.save()

        grupo_profissional = Group.objects.get(name='profissionais de saude')
        usuario.groups.add(grupo_profissional)

        assunto = 'Sistema Médico Pericial - UFAC - Confirmação de Cadastro'
        message = f'Olá {profissional.nome}! Seu cadastro foi confirmado com sucesso! ' \
                  f'Seu login é o seu CPF. \n Por favor, clique no link abaixo para ' \
                  f'redefinir sua senha: \n www.google.com.br'
        try:
            send_mail(assunto, message, EMAIL_HOST_USER, [email])
            msg = 'Cadastrado com sucesso! Enviamos um e-mail de recuperação de senha.'
        except:
            msg = 'Cadastro realizado com sucesso!'

        if self.is_ajax():
            return JsonResponse({'success': True, 'message': msg})

        messages.success(self.request, msg)
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors})
        messages.error(self.request, 'Erro! Verifique os campos preenchidos e tente novamente.')
        return super().form_invalid(form)



# class AgendamentoCreate(CreateView):
#     model = Agendamento
#     form_class = AgendamentoForm
#     template_name = 'consultas/listagem_agendamentos.html'
#     success_url = reverse_lazy('agendamentoListagem')

#     def form_valid(self, form):
#         self.object = form.save()
#         agendamento_data = {
#             'paciente': self.object.paciente.nome,
#             'profissional_saude': self.object.profissional_saude.nome,
#             'data_agendamento': self.object.data_agendamento.strftime('%d/%m/%Y'),
#             'turno': self.object.get_turno_display(),
#             'prioridade_atendimento': 'Sim' if self.object.prioridade_atendimento else 'Não',
#             'download_url': reverse_lazy('downloadComprovante', kwargs={'pk': self.object.pk})
#         }
#         return JsonResponse({'success': True, 'agendamento': agendamento_data})

#     def form_invalid(self, form):
#         messages.error(self.request, 'Erro ao realizar o agendamento. Verifique os dados e tente novamente.')
#         print("Erro ao realizar o agendamento.")
#         print(form.errors)  

#         # Se a solicitação for AJAX, retorna um JSON com os erros
#         if self.request.is_ajax():
#             errors = form.errors.as_json()
#             return JsonResponse({'success': False, 'errors': errors}, status=400)

#         # Renderizar o template novamente com o formulário inválido
#         return self.render_to_response(self.get_context_data(form=form))
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['messages'] = messages.get_messages(self.request)
#         return context
    
#     def generate_pdf(self, agendamento):
#         html_content = render_to_string('consultas/comprovantePdf_agendamento.html', {'agendamento': agendamento})

#         pdf_file = io.BytesIO()
#         pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

#         if pisa_status.err:
#             raise Exception("Erro ao gerar PDF.")

#         pdf_file.seek(0)
#         return pdf_file
    
    
    
    
class AgendamentoCreate(CreateView):
    model = Agendamento
    form_class = AgendamentoForm
    template_name = 'consultas/listagem_agendamentos.html'
    success_url = reverse_lazy('agendamentoListagem')

    def form_valid(self, form):
        self.object = form.save()
        agendamento_data = {
            'paciente': self.object.paciente.get_display_name(),
            'profissional_saude': self.object.profissional_saude.get_display_name(),
            'data_agendamento': self.object.data_agendamento.strftime('%d/%m/%Y'),
            'turno': self.object.get_turno_display(),
            'prioridade_atendimento': 'Sim' if self.object.prioridade_atendimento else 'Não',
            'download_url': reverse_lazy('downloadComprovante', kwargs={'pk': self.object.pk})
        }
        return JsonResponse({'success': True, 'agendamento': agendamento_data})

    def form_invalid(self, form):
        # Corrigindo a estrutura de retorno de erros para um objeto JSON adequado
        errors = form.errors.get_json_data()
        print(f"Erros no form_invalid: {errors}")
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context




def download_comprovante(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)

    html_content = render_to_string('consultas/comprovantePdf_agendamento.html', {'agendamento': agendamento})

    pdf_file = io.BytesIO()
    pisa.CreatePDF(html_content, dest=pdf_file)

    pdf_file.seek(0)

    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=Comprovante_Agendamento_{agendamento.id}.pdf'

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

from django.utils import timezone

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
        context['receita_medica_form'] = ReceitaMedicaForm()
        context['laudo_form'] = LaudoForm(agendamento=agendamento) 
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        agendamento_id = self.kwargs['agendamento_id']
        agendamento = get_object_or_404(Agendamento, id=agendamento_id)
        
        atendimento_form = AtendimentoForm(request.POST, request.FILES)
        atestado_medico_form = AtestadoMedicoForm(request.POST, agendamento=agendamento)
        receita_medica_form = ReceitaMedicaForm(request.POST, agendamento=agendamento)
        laudo_form = LaudoForm(request.POST, agendamento=agendamento)
        
        if atendimento_form.is_valid():
            return self.form_valid(atendimento_form, atestado_medico_form, receita_medica_form, laudo_form, agendamento)
        else:
            return self.form_invalid(atendimento_form, atestado_medico_form, receita_medica_form, laudo_form)

    def form_valid(self, atendimento_form, atestado_medico_form, receita_medica_form, laudo_form, agendamento):
        atendimento = atendimento_form.save(commit=False)
        atendimento.agendamento = agendamento

        # Salvar o início do atendimento
        atendimento.inicio_atendimento = timezone.now()
        atendimento.save()

        agendamento.status_atendimento = 'atendido'
        agendamento.save()

        if atestado_medico_form.is_valid():
            atestado_medico = atestado_medico_form.save(commit=False)
            dias_afastamento = atestado_medico_form.cleaned_data.get('dias_afastamento')
            atestado_medico.texto_padrao = atestado_medico.texto_padrao.replace('[[DIAS]]', str(dias_afastamento))
            atestado_medico.agendamento = agendamento
            atestado_medico.save()
        
        if receita_medica_form.is_valid():
            receita_medica = receita_medica_form.save(commit=False)
            receita_medica.agendamento = agendamento
            receita_medica.save()

        if laudo_form.is_valid():
            laudo = laudo_form.save(commit=False)
            laudo.agendamento = agendamento
            laudo.save()

        return redirect('confirmar_atendimento', agendamento_id=agendamento.id)

    def form_invalid(self, atendimento_form, atestado_medico_form, receita_medica_form, laudo_form):
        context = self.get_context_data()
        context['form'] = atendimento_form
        context['atestado_medico_form'] = atestado_medico_form
        context['receita_medica_form'] = receita_medica_form
        context['laudo_form'] = laudo_form
        return self.render_to_response(context)


def confirmar_atendimento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)
    atendimento = get_object_or_404(Atendimento, agendamento=agendamento)

    # Salvar o fim do atendimento, se ainda não estiver definido
    if not atendimento.fim_atendimento:
        atendimento.fim_atendimento = timezone.now()
        atendimento.save()

    # Buscar as receitas médicas
    receita_simples = ReceitaMedica.objects.filter(agendamento=agendamento, tipo='simples').first()
    receita_controle_especial = ReceitaMedica.objects.filter(agendamento=agendamento, tipo='controle_especial').first()

    laudos = Laudo.objects.filter(agendamento=agendamento).order_by('-data_laudo')

    # Verificar se os campos essenciais estão preenchidos
    mostrar_receita_simples = receita_simples and (receita_simples.prescricao or receita_simples.dosagem or receita_simples.via_administrativa or receita_simples.modo_uso)
    mostrar_receita_controle_especial = receita_controle_especial and (receita_controle_especial.prescricao or receita_controle_especial.dosagem or receita_controle_especial.via_administrativa or receita_controle_especial.modo_uso)

    return render(request, 'consultas/confirmar_atendimento.html', {
        'atendimento': atendimento,
        'receita_simples': receita_simples if mostrar_receita_simples else None,
        'receita_controle_especial': receita_controle_especial if mostrar_receita_controle_especial else None,
        'laudos': laudos,
    })


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
    response['Content-Disposition'] = f'inline; filename=comprovante_atendimento_{atendimento_id}.pdf'
    
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
    profissionais_saude = Profissionaldasaude.objects.all()

    # Verificar as receitas associadas aos atendimentos
    prontuario_dados = []
    for atendimento in atendimentos:
        agendamento = atendimento.agendamento
        receita_simples = ReceitaMedica.objects.filter(agendamento=agendamento, tipo='simples').first()
        receita_controle_especial = ReceitaMedica.objects.filter(agendamento=agendamento, tipo='controle_especial').first()

        mostrar_receita_simples = receita_simples and (
            receita_simples.prescricao or receita_simples.dosagem or receita_simples.via_administrativa or receita_simples.modo_uso
        )
        mostrar_receita_controle_especial = receita_controle_especial and (
            receita_controle_especial.prescricao or receita_controle_especial.dosagem or receita_controle_especial.via_administrativa or receita_controle_especial.modo_uso
        )

        prontuario_dados.append({
            'atendimento': atendimento,
            'receita_simples': receita_simples if mostrar_receita_simples else None,
            'receita_controle_especial': receita_controle_especial if mostrar_receita_controle_especial else None,
        })

    return render(request, 'consultas/prontuario_medico.html', {
        'paciente': paciente,
        'prontuario_dados': prontuario_dados,
        'profissionais_saude': profissionais_saude,
    })


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
    paciente_nome = paciente.nome.replace(' ', '_').lower()
    medicos_ids = request.GET.get('medicos')
    atendimentos_ids = request.GET.get('atendimentos')

    if medicos_ids:
        medicos_ids = [int(id) for id in medicos_ids.split(",")]

        ids_agendamentos = paciente.agendamento_set.filter(profissional_saude__id__in=medicos_ids).values_list('id', flat=True)
        atendimentos = Atendimento.objects.filter(agendamento__id__in=ids_agendamentos)
    else:
        atendimentos = Atendimento.objects.filter(agendamento__paciente=paciente)

    if atendimentos_ids:
        atendimentos_ids = [int(id) for id in atendimentos_ids.split(",")]
        atendimentos = atendimentos.filter(id__in=atendimentos_ids)

    prontuario_dados = []
    for atendimento in atendimentos:
        agendamento = atendimento.agendamento
        receita_simples = ReceitaMedica.objects.filter(agendamento=agendamento, tipo='simples').first()
        receita_controle_especial = ReceitaMedica.objects.filter(agendamento=agendamento, tipo='controle_especial').first()

        mostrar_receita_simples = receita_simples and (
            receita_simples.prescricao or receita_simples.dosagem or receita_simples.via_administrativa or receita_simples.modo_uso
        )
        mostrar_receita_controle_especial = receita_controle_especial and (
            receita_controle_especial.prescricao or receita_controle_especial.dosagem or receita_controle_especial.via_administrativa or receita_controle_especial.modo_uso
        )

        prontuario_dados.append({
            'atendimento': atendimento,
            'receita_simples': receita_simples if mostrar_receita_simples else None,
            'receita_controle_especial': receita_controle_especial if mostrar_receita_controle_especial else None,
        })

    context = {
        'paciente': paciente,
        'prontuario_dados': prontuario_dados,
        'medicos_ids': medicos_ids,
    }

    html = render_to_string('pdfs/pdf_prontuario_medico.html', context)

    # WeasyPrint para transformar o HTML em PDF.
    pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="prontuario_{paciente_nome}.pdf"'
    return response

def pdf_atestado_medico(request, atendimento_id):
    atendimento = get_object_or_404(Atendimento, id=atendimento_id)
    agendamento = atendimento.agendamento
    atestado = get_object_or_404(AtestadoMedico, agendamento=agendamento)
    paciente_nome = atestado.paciente.nome.replace(' ', '_').lower()
    
    context = {
        'atendimento': atendimento,
        'atestado': atestado,
    }

    html = render_to_string('pdfs/pdf_atestado_medico.html', context)
    
    # Cria um arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(target=temp_pdf.name)
        
        # Lê o conteúdo do arquivo temporário
        temp_pdf.seek(0)
        pdf_content = temp_pdf.read()

    # Remove o arquivo temporário
    os.remove(temp_pdf.name)
    
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="atestado_{paciente_nome}.pdf"'
    return response

def pdf_receita_medica(request, atendimento_id, tipo=None):
    atendimento = get_object_or_404(Atendimento, id=atendimento_id)
    agendamento = atendimento.agendamento
    receita = get_object_or_404(ReceitaMedica, agendamento=agendamento)
    paciente_nome = receita.paciente.nome.replace(' ', '_').lower()

    context = {
        'atendimento': atendimento,
        'receita': receita,
    }

    # Verifica o tipo de receita para escolher o template correto
    if tipo == 'controle_especial' or receita.tipo == 'controle_especial':
        template_path = 'pdfs/pdf_receita_medica_controle.html'
        css = CSS(string='@page { size: A4 landscape; }')
    else:
        template_path = 'pdfs/pdf_receita_medica.html'
        css = None

    html = render_to_string(template_path, context)
    
    # Cria um arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(target=temp_pdf.name, stylesheets=[css] if css else [])
        
        # Lê o conteúdo do arquivo temporário
        temp_pdf.seek(0)
        pdf_content = temp_pdf.read()

    # Remove o arquivo temporário
    os.remove(temp_pdf.name)
    
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="receita_{paciente_nome}.pdf"'
    return response


def pdf_laudo_medico(request, atendimento_id):
    atendimento = get_object_or_404(Atendimento, id=atendimento_id)
    agendamento = atendimento.agendamento
    laudo = get_object_or_404(Laudo, agendamento=agendamento)
    paciente_nome = laudo.paciente.nome.replace(' ', '_').lower()
    
    context = {
        'atendimento': atendimento,
        'laudo': laudo,
    }

    html = render_to_string('pdfs/pdf_laudo_medico.html', context)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(target=temp_pdf.name)
        
        temp_pdf.seek(0)
        pdf_content = temp_pdf.read()

    os.remove(temp_pdf.name)
    
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="laudo_{paciente_nome}.pdf"'
    return response


def excluir_arquivo(request, arquivo_id, atendimento_id):
    arquivo = get_object_or_404(ArquivoPaciente, id=arquivo_id)

    if request.method == 'POST':
        arquivo.delete()
        messages.success(request, 'Arquivo excluído!')
        return redirect('visualizarAtendimento', atendimento_id=atendimento_id)
    else:
        messages.error(request, 'Falha ao excluir o arquivo! Tente novamente.')

    return redirect('visualizarAtendimento', atendimento_id=atendimento_id)








