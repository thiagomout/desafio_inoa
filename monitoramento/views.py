from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Ativo, TunelDePreco, HistoricoPreco
from .forms import AtivoForm, TunelDePrecoForm
from .forms import CustomUserCreationForm
from django.contrib import messages
import yfinance as yf
from decimal import Decimal, InvalidOperation

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def home(request):
    return render(request, 'monitoramento/home.html')

@login_required
def dashboard(request):
    ativos = Ativo.objects.filter(user=request.user).prefetch_related('tuneldepreco')
    ativo_form = AtivoForm(user=request.user)
    tunel_form = TunelDePrecoForm(user=request.user)
    
    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST.get('action')
            ativo_id = request.POST.get('ativo_id')

            if action == 'save_changes':
                ativo = get_object_or_404(Ativo, id=ativo_id, user=request.user)
                
                # Salva o intervalo do ativo
                ativo.intervalo_checagem = request.POST.get('intervalo_checagem')
                ativo.save()

                # Atualiza o túnel
                if hasattr(ativo, 'tuneldepreco') and ativo.tuneldepreco:
                    tunel = ativo.tuneldepreco
                    
                    # Pega os valores do POST
                    preco_min_str = request.POST.get('preco_min')
                    preco_max_str = request.POST.get('preco_max')
                    
                    if preco_min_str and preco_max_str:
                        try:
                            # A CORREÇÃO ESTÁ AQUI: Substitui a vírgula pelo ponto
                            preco_min_limpo = preco_min_str.replace(',', '.')
                            preco_max_limpo = preco_max_str.replace(',', '.')

                            # Converte para Decimal e salva
                            tunel.preco_min = Decimal(preco_min_limpo)
                            tunel.preco_max = Decimal(preco_max_limpo)
                            tunel.save()
                        except InvalidOperation:
                            # Lida com o caso de o usuário digitar algo que não é um número
                            messages.error(request, "Por favor, insira um valor numérico válido para os preços.")
                
                return redirect('dashboard')

            elif action == 'delete_ativo':
                ativo = get_object_or_404(Ativo, id=ativo_id, user=request.user)
                ativo.delete()
                return redirect('dashboard')

            elif action == 'delete_tunel':
                tunel_id = request.POST.get('tunel_id')
                tunel = get_object_or_404(TunelDePreco, id=tunel_id, ativo__user=request.user)
                tunel.delete()
                return redirect('dashboard')

        elif 'add_ativo' in request.POST:
            ativo_form = AtivoForm(request.POST, user=request.user)
            if ativo_form.is_valid():
                novo_ativo = ativo_form.save(commit=False)
                novo_ativo.user = request.user
                novo_ativo.save()
                return redirect('dashboard')

        elif 'add_tunel' in request.POST:
            tunel_form = TunelDePrecoForm(request.POST, user=request.user)
            if tunel_form.is_valid():
                tunel_form.save()
                return redirect('dashboard')

    
    show_tunel_form_first = Ativo.objects.filter(user=request.user, tuneldepreco__isnull=True).exists()

    context = {
        'ativos': ativos,
        'ativo_form': ativo_form,
        'tunel_form': tunel_form,
        'show_tunel_form_first': show_tunel_form_first,
    }
    return render(request, 'monitoramento/dashboard.html', context)

@login_required
def ativo_detalhe(request, ativo_id):
    ativo = get_object_or_404(Ativo, id=ativo_id, user=request.user)
    historico = HistoricoPreco.objects.filter(ativo=ativo)
    
    preco_atual = "N/A"
    try:
        # Adiciona ".SA" para buscar tickers da B3
        ticker = yf.Ticker(f"{ativo.ticker}.SA")
        dados_hoje = ticker.history(period='1d')
        if not dados_hoje.empty:
            preco_atual = dados_hoje['Close'].iloc[-1]
    except Exception as e:
        print(f"Erro ao buscar cotação para {ativo.ticker}: {e}")

    context = {
        'ativo': ativo,
        'preco_atual': preco_atual,
        'historico': historico,
    }
    return render(request, 'monitoramento/ativo_detalhe.html', context)