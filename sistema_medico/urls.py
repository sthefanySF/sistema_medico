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

   

    path('fila_de_espera/', fila_espera, name='fila_espera'),
    path('cadastro/administrativo/', AdministrativoCreate.as_view(), name='administrativoCreate'),
    path('cadastro/profissionaldasaude/', ProfissionaldasaudeCreate.as_view(), name='profissionaldasaudeCreate'),
    path('fila-de-espera/', fila_espera, name='fila_espera'),
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
    path('agendamentos/<int:pk>/editar/', agendamento_editar, name='agendamentoEditar'),
    path('agendamentos/<int:pk>/confirmar/', agendamento_confirmar, name='agendamentoConfirmar'),
    path('agendamentos/<int:pk>/ausente/', agendamento_ausente, name='agendamentoAusente'),

    path('', views.home, name='home'),


]