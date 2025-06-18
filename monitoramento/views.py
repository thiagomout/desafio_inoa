from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Ativo
from .forms import AtivoForm
from .forms import CustomUserCreationForm

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
    ativos = Ativo.objects.filter(user=request.user)

    if request.method == 'POST':
        form = AtivoForm(request.POST)
        if form.is_valid():
            novo_ativo = form.save(commit=False)
            novo_ativo.user = request.user
            novo_ativo.save()
            return redirect('dashboard')
    else:
        form = AtivoForm()

    return render(request, 'monitoramento/dashboard.html', {
        'ativos': ativos,
        'form': form
    })