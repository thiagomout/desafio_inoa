from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ativo/<int:ativo_id>/', views.ativo_detalhe, name='ativo_detalhe'),
]
