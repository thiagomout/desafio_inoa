from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Ativo, TunelDePreco
from .forms import AtivoForm, TunelDePrecoForm
from .forms import CustomUserCreationForm
from django.contrib import messages



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
        # Ações da tabela de ativos (Salvar, Remover Ativo, Remover Túnel)
        if 'action' in request.POST:
            action = request.POST.get('action')
            ativo_id = request.POST.get('ativo_id')

            if action == 'save_changes':
                ativo = get_object_or_404(Ativo, id=ativo_id, user=request.user)
                ativo_edit_form = AtivoForm(request.user, request.POST, instance=ativo)
                if ativo_edit_form.is_valid():
                    ativo_edit_form.save()

                # Se o ativo tiver um túnel, atualizá-lo
                if hasattr(ativo, 'tuneldepreco') and ativo.tuneldepreco:
                    tunel_edit_form = TunelDePrecoForm(request.user, request.POST, instance=ativo.tuneldepreco)
                    if tunel_edit_form.is_valid():
                         tunel_edit_form.save()
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

        # Formulário para adicionar novo ativo
        elif 'add_ativo' in request.POST:
            ativo_form = AtivoForm(request.user, request.POST)
            if ativo_form.is_valid():
                novo_ativo = ativo_form.save(commit=False)
                novo_ativo.user = request.user
                novo_ativo.save()
                return redirect('dashboard')

        # Formulário para adicionar novo túnel
        elif 'add_tunel' in request.POST:
            tunel_form = TunelDePrecoForm(request.user, request.POST)
            if tunel_form.is_valid():
                tunel_form.save()
                return redirect('dashboard')

    context = {
        'ativos': ativos,
        'ativo_form': ativo_form,
        'tunel_form': tunel_form,
    }
    return render(request, 'monitoramento/dashboard.html', context)