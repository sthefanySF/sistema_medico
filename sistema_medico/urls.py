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
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # HOME. Login and Logout
    # path('login/', logar, name='login'),
    path('', logar, name='login'),
    path('logout/', sair, name='sair'),
    
    # Recuperar senha
    path('login/', include('login.urls')),

    # Cadastro
    path('cadastro/administrativo/', AdministrativoCreate.as_view(), name='administrativoCreate'),
    path('cadastro/profissionaldasaude/', ProfissionaldasaudeCreate.as_view(), name='profissionaldasaudeCreate'),
    path('cadastro/paciente/', PacienteCreate.as_view(), name='pacienteCreate'),
    
    # Agendamento
    path('agendamento/form', AgendamentoCreate.as_view(), name='agendamentoCreate' ),
    path('agendamento/lista', listar_agendamentos, name='agendamentoListagem'),
    path('agendamentos/<int:pk>/confirmar/', agendamento_confirmar, name='agendamentoConfirmar'),
    path('agendamentos/<int:pk>/ausente/', agendamento_ausente, name='agendamentoAusente'),
    path('agendamento/<int:pk>/confirmar/', confirm_agendamento, name='confirmAgendamento'),
    path('agendamento/<int:pk>/download/', download_comprovante, name='downloadComprovante'),
    path('cancelar_agendamento/<int:agendamento_id>/', cancelar_agendamento, name='cancelar_agendamento'),
    path('reagendar/agendamento/<int:pk>/', reagendar_agendamento, name='reagendarAgendamento'),
    path('comprovante/cancelamento/<int:agendamento_id>/', views.pdf_comprovante_cancelamento, name='comprovante_cancelamento'),
    path('agendamentos/cancelados/', listar_agendamentos_cancelados, name='listar_agendamentos_cancelados'),
    
    # Atendimento
    path('atendimento/criar/<int:agendamento_id>', AtendimentoCreate.as_view(), name='criar_atendimento'),
    path('atendimentos/', lista_atendimentos, name='listaAtendimentos'),
    path('atendimento/<int:pk>/', VisualizarAtendimentoView.as_view(), name='visualizarAtendimento'),
    path('confirmar_atendimento/<int:agendamento_id>/', confirmar_atendimento, name='confirmar_atendimento'),

    path('download_comprovante_atendimento/<int:atendimento_id>/', download_comprovante_atendimento,
         name='download_comprovante_atendimento'),

    path('visualizar_comprovante_atendimento/<int:atendimento_id>/', views.visualizar_comprovante_atendimento,
         name='visualizar_comprovante_atendimento'),
    path('registrar_inicio_atendimento/<int:agendamento_id>/', registrar_inicio_atendimento, name='registrar_inicio_atendimento'),
    path('consultas/manter_em_atendimento/<int:agendamento_id>/', views.manter_em_atendimento, name='manter_em_atendimento'),
    path('atendimentos/<int:agendamento_id>/cancelar/', cancelar_atendimento, name='cancelar_atendimento'),
    
    # Prontuario
    path('prontuario_medico/<int:paciente_id>/', views.prontuario_medico, name='prontuario_medico'),
    path('filtrar_prontuarios/', filtrar_prontuarios, name='filtrar_prontuarios'),
    

    #pdfs
    path('visualizar-pdf-exames/<int:atendimento_id>/', views.visualizar_pdf_exames, name='visualizar_pdf_exames'),
    path('pdf_prontuario_medico/<int:paciente_id>/', views.pdf_prontuario_medico, name='pdf_prontuario_medico'),
    path('atendimento/<int:atendimento_id>/atestado/', pdf_atestado_medico, name='pdf_atestado_medico'),
    path('atendimento/<int:atendimento_id>/receita/', pdf_receita_medica, name='pdf_receita_medica'),
    path('pdf_receita_medica/<int:atendimento_id>/<str:tipo>/', pdf_receita_medica, name='pdf_receita_medica_controle'),
    path('pdf_laudo/<int:atendimento_id>/', pdf_laudo_medico, name='pdf_laudo_medico'),


    
    # Listagens
    path('pacientes/', listar_pacientes, name= 'pacienteListagem' ),
    path('profissionaldasaude/', listar_profissionaldasaude, name= 'profissionaldasaudeListagem'),
    path('administrativo/', listar_administrativo, name= 'administrativoListagem'),

    # Edição e Exclusão
    path('paciente/<int:pk>/editar/', paciente_editar, name='pacienteEditar'),
    path('paciente/<int:pk>/excluir/', paciente_excluir, name='pacienteExcluir'),
    path('administrativo/<int:pk>/editar/', administrativo_editar, name='administrativoEditar'),
    path('administrativo/<int:pk>/excluir/', administrativo_excluir, name='administrativoExcluir'),
    path('profissionaldasaude/<int:pk>/editar/', profissionaldasaude_editar, name='profissionaldasaudeEditar'),
    path('profissionaldasaude/<int:pk>/excluir/', profissionaldasaude_excluir, name='profissionaldasaudeExcluir'),
    
    path('editar_administrativo/', views.editar_administrativo, name='editar_administrativo'),#modal editar
    path('editar_paciente/', views.editar_paciente, name='editar_paciente'),#modal editar
    path('editar_profissionaldasaude/', views.editar_profissionaldasaude, name='editar_profissionaldasaude'),#modal editar


    # Restrição de acesso
    path('restricao/', restricao_de_acesso, name='restricao_de_acesso'),
    path('atendimento/<int:atendimento_id>/atualizar_privado/', atualizar_privado, name='atualizar_privado'),
    
    # Excluir arquivos de pacientes enviados em 'Atendimentos'
    path('arquivo/excluir/<int:arquivo_id>/<int:atendimento_id>/', excluir_arquivo, name='excluir_arquivo'),
    
    
    path('search_paciente/', views.search_paciente, name='search_paciente'),
    path('search_profissional/', views.search_profissional, name='search_profissional'),
    
    path('relatorios/', views.obter_relatorios, name='relatorios'),

    # Home
    # path('', views.home, name='home'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)