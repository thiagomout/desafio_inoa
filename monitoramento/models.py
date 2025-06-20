from django.db import models
from django.contrib.auth.models import User

class Ativo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10)

    INTERVALO_CHOICES = [
        (1, '1 minuto'),
        (5, '5 minutos'),
        (15, '15 minutos'),
        (30, '30 minutos'),
        (60, '1 hora'),
    ]
    intervalo_checagem = models.PositiveIntegerField(choices=INTERVALO_CHOICES, default=5, verbose_name='Intervalo de Checagem (minutos)')
    ultima_checagem = models.DateTimeField(null=True, blank=True, verbose_name='Última Checagem')
    estado = models.IntegerField(default=0, verbose_name='Estado do Ativo (0: neutro, -1: abaixo do túnel, 1: acima do túnel)')

    class Meta:
        unique_together = ('user', 'ticker')

    def __str__(self):
        return f'{self.nome} ({self.ticker})'

class TunelDePreco(models.Model):
    ativo = models.OneToOneField(Ativo, on_delete=models.CASCADE)
    preco_min = models.DecimalField(max_digits=10, decimal_places=2)
    preco_max = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Túnel: {self.preco_min} - {self.preco_max} ({self.ativo.ticker})'

class HistoricoPreco(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.CASCADE, related_name='historico')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.ativo.ticker} - {self.preco} em {self.timestamp.strftime('%d/%m/%Y %H:%M')}"
