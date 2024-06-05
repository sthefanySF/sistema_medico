"""
URL configuration for sistema_medico project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from consulta.views import *
from consulta import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # Login
    path('login/', logar, name='login'),
    path('logout/', sair, name='sair'),

    # Recuperar senha
    path('login/', include('login.urls')),


    path('cadastro/administrativo/', AdministrativoCreate.as_view(), name='administrativoCreate'),

    path('cadastro/profissionaldasaude/', ProfissionaldasaudeCreate.as_view(), name='profissionaldasaudeCreate'),
    # path('cadastro/profissionaldasaude/', ProfissionaldasaudeCreate.as_view(), name='profissionaldasaudeCreate'),

    path('cadastro/paciente', PacienteCreate.as_view(), name='pacienteCreate'),

    path('agendamento/form', AgendamentoCreate.as_view(), name='agendamentoCreate' ),
    path('agendamento/lista', listar_agendamentos, name='agendamentoListagem'),

    path('pacientes/', listar_pacientes, name= 'pacienteListagem' ),
    path('profissionaldasaude/', listar_profissionaldasaude, name= 'profissionaldasaudeListagem'),
    path('administrativo/', listar_administrativo, name= 'administrativoListagem'),
    path('paciente/<int:pk>/editar/', paciente_editar, name='pacienteEditar'),
    path('paciente/<int:pk>/excluir/', paciente_excluir, name='pacienteExcluir'),
    path('administrativo/<int:pk>/editar/', administrativo_editar, name='administrativoEditar'),
    path('administrativo/<int:pk>/excluir/', administrativo_excluir, name='administrativoExcluir'),
    path('profissionaldasaude/<int:pk>/editar/', profissionaldasaude_editar, name='profissionaldasaudeEditar'),
    path('profissionaldasaude/<int:pk>/excluir/', profissionaldasaude_excluir, name='profissionaldasaudeExcluir'),
    path('agendamentos/<int:pk>/confirmar/', agendamento_confirmar, name='agendamentoConfirmar'),
    path('agendamentos/<int:pk>/ausente/', agendamento_ausente, name='agendamentoAusente'),
    path('reagendar/agendamento/<int:pk>/', views.reagendar_agendamento, name='reagendarAgendamento'),
    path('cancelar_agendamento/<int:agendamento_id>/', cancelar_agendamento, name='cancelar_agendamento'),
    path('atendimento/criar/<int:agendamento_id>', AtendimentoCreate.as_view(), name='criar_atendimento'),
    path('atendimentos/', lista_atendimentos, name='listaAtendimentos'),
    path('atendimentos/<int:atendimento_id>/', visualizar_atendimento, name='visualizarAtendimento'),
    # path('login/', user_login, name='login'),
    path('agendamento/<int:pk>/confirmar/', confirm_agendamento, name='confirmAgendamento'),
    path('agendamento/<int:pk>/download/', download_comprovante, name='downloadComprovante'),
    path('confirmar-atendimento/<int:agendamento_id>/', confirmar_atendimento, name='confirmar_atendimento'),
    path('download-comprovante-atendimento/<int:atendimento_id>/', download_comprovante_atendimento, name='download_comprovante_atendimento'),
    path('visualizar-pdf-exames/<int:atendimento_id>/', views.visualizar_pdf_exames, name='visualizar_pdf_exames'),
    path('visualizar-comprovante-atendimento/<int:atendimento_id>/', views.visualizar_comprovante_atendimento, name='visualizar_comprovante_atendimento'),
    # path('prontuario/', prontuario_medico, name='prontuario_medico'),
    path('prontuario_medico/<int:paciente_id>/', views.prontuario_medico, name='prontuario_medico'),
    path('filtrar_prontuarios/', filtrar_prontuarios, name='filtrar_prontuarios'),
    path('atestado_medico/<int:paciente_id>/', views.atestado_medico, name='atestado_medico'),
    
    # pdfs  
    path('pdf_prontuario_medico/<int:paciente_id>/', views.pdf_prontuario_medico, name='pdf_prontuario_medico'),
    
    # path('cancelar/agendamento/<int:pk>/', views.cancelar_agendamento, name='cancelarAgendamento'),
    path('', views.home, name='home'),


]