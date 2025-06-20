from django import forms
from .models import Ativo, TunelDePreco
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class AtivoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Correção: Extrair 'user' dos kwargs.
        self.user = kwargs.pop('user', None)
        super(AtivoForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Ativo
        fields = ['nome', 'ticker', 'intervalo_checagem']

    def clean_ticker(self):
        # Corrigido para usar self.instance para edições
        cleaned_data = super().clean()
        ticker = cleaned_data.get('ticker').upper()
        instance = self.instance

        if self.user and Ativo.objects.filter(user=self.user, ticker=ticker).exclude(pk=instance.pk if instance else None).exists():
            raise ValidationError('Você já está monitorando esse ticker.')

        return ticker


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email") # Removido password, UserCreationForm já cuida disso


class TunelDePrecoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Correção: Mudar a assinatura e extrair 'user' dos kwargs.
        self.user = kwargs.pop('user', None)
        super(TunelDePrecoForm, self).__init__(*args, **kwargs)
        if self.user:
            # Filtra apenas os ativos do usuário logado
            self.fields['ativo'].queryset = Ativo.objects.filter(user=self.user)

    class Meta:
        model = TunelDePreco
        fields = ['ativo', 'preco_min', 'preco_max']