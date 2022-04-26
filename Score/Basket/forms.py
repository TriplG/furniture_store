from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import *


class AllProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description']


class Message(forms.ModelForm):
    class Meta:
        # model = Coments_Answer
        fields = ['message']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))