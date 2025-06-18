from django import forms
from .models import Ativo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AtivoForm(forms.ModelForm):
    class Meta:
        model = Ativo
        fields = ['nome', 'ticker']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")