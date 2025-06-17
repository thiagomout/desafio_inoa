from django.core.management.base import BaseCommand
from monitoramento.models import Ativo, TunelDePreco, ConfiguracaoChecagem
import random  # Por enquanto, simulação

class Command(BaseCommand):
    help = 'Checa as cotações dos ativos e compara com os limites definidos'

    def handle(self, *args, **kwargs):
        ativos = Ativo.objects.all()

        for ativo in ativos:
            try:
                tunel = TunelDePreco.objects.get(ativo=ativo)
                config = ConfiguracaoChecagem.objects.get(ativo=ativo)

                # Simulação de cotação atual (exemplo: de 10 a 50 reais)
                cotacao_atual = random.uniform(10.0, 50.0)
                print(f'Ativo {ativo.ticker} - Cotação atual: {cotacao_atual:.2f}')

                if cotacao_atual < float(tunel.preco_min):
                    print(f'ALERTA: {ativo.ticker} abaixo do limite mínimo ({tunel.preco_min})')
                elif cotacao_atual > float(tunel.preco_max):
                    print(f'ALERTA: {ativo.ticker} acima do limite máximo ({tunel.preco_max})')
                else:
                    print(f'{ativo.ticker} dentro do túnel')

            except TunelDePreco.DoesNotExist:
                print(f'Túnel de preço não configurado para {ativo.ticker}')
            except ConfiguracaoChecagem.DoesNotExist:
                print(f'Configuração de checagem não encontrada para {ativo.ticker}')
