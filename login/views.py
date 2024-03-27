# _*_coding:utf-8_*_


from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import  force_bytes
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, get_user_model
from django.utils.encoding import force_str

from sistema_medico.settings import EMAIL_HOST_USER
from .forms import *

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy


def redefinir_senha(request):
    form = AlterarSenhaForm()
    if request.method == 'POST':
        email = request.POST.get('email')
        form = AlterarSenhaForm(request.POST)
        if form.is_valid():
            try:
                usuario = User.objects.get(email=email)
                form = PasswordResetForm({'email': usuario.email})
                form.full_clean()

            except:
                messages.error(request, 'E-mail não localizado! Tente novamente.')
                return TemplateResponse(request, 'login/redefinir_senha.html', locals())

            opts = {
                'domain_override': request.META['HTTP_HOST'],
                'use_https': request.is_secure(),
                'from_email': EMAIL_HOST_USER,
                'email_template_name': 'login/redefinir_senha_email.html',
                'subject_template_name': 'login/redefinir_senha.txt',
                'request': request,
            }
            form.save(**opts)
            context = {
                'form': form,
                'uid': usuario.id,
                'token': default_token_generator,
            }

            return HttpResponseRedirect(reverse_lazy('redefinir_senha_ok'))
    return TemplateResponse(request, 'login/redefinir_senha.html', locals())


def redefinir_senha_ok(request):
    return TemplateResponse(request, 'login/redefinir_senha_ok.html', locals())



def redefinir_senha_confirmacao(request, token, uidb64):
    user_model = get_user_model()
    assert uidb64 is not None and token is not None
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user_model._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse_lazy('redefinir_senha_completa'))
        else:
            form = SetPasswordForm(None)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }
    return TemplateResponse(request, 'login/redefinir_senha_confirmacao.html', locals())


def redefinir_senha_completa(request):
    return TemplateResponse(request, 'login/redefinir_senha_completa.html', locals())


