from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView

from .views import *

urlpatterns = [

    path('redefinir_senha/', redefinir_senha, name='redefinir_senha'),
    path('redefinir_senha/ok/', redefinir_senha_ok, name='redefinir_senha_ok'),

    path('redefinir_senha/<uidb64>/<token>/', redefinir_senha_confirmacao, name='redefinir_senha_confirmacao'),
    path('redefinir_senha/completa/', redefinir_senha_completa, name='redefinir_senha_completa'),







]




