# -*- coding: UTF-8 -*-


from django.contrib.auth.models import User
from django.forms import *
from django import forms



# Form para manipulação personalizada
class AlterarSenhaForm(forms.Form):
    email = CharField(widget=forms.TextInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        super(AlterarSenhaForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
