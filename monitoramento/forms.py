from django import forms
from .models import Ativo, TunelDePreco
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AtivoForm(forms.ModelForm):
    class Meta:
        model = Ativo
        fields = ['nome', 'ticker']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pegando o usuário que chamou
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        ticker = cleaned_data.get('ticker')

        if ticker and Ativo.objects.filter(user=self.user, ticker=ticker).exists():
            self.add_error('ticker', 'Você já está monitorando esse ticker.')

        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class TunelDePrecoForm(forms.ModelForm):
    class Meta:
        model = TunelDePreco
        fields = ['ativo', 'preco_min', 'preco_max']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas os ativos do usuário logado
        self.fields['ativo'].queryset = user.ativo_set.all()