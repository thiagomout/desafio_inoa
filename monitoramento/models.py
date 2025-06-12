from django.db import models

class Ativo(models.Model):
    nome = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.nome} ({self.ticker})'

class TunelDePreco(models.Model):
    ativo = models.OneToOneField(Ativo, on_delete=models.CASCADE)
    preco_min = models.DecimalField(max_digits=10, decimal_places=2)
    preco_max = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Túnel: {self.preco_min} - {self.preco_max} ({self.ativo.ticker})'

class ConfiguracaoChecagem(models.Model):
    ativo = models.OneToOneField(Ativo, on_delete=models.CASCADE)
    intervalo_minutos = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.ativo.ticker} - a cada {self.intervalo_minutos} min'
