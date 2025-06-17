from django.core.management.base import BaseCommand
from monitoramento.models import Ativo, TunelDePreco, ConfiguracaoChecagem
import yfinance as yf
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Checa as cotações dos ativos e compara com os limites definidos'

    def handle(self, *args, **kwargs):
        ativos = Ativo.objects.all()

        for ativo in ativos:
            try:
                tunel = TunelDePreco.objects.get(ativo=ativo)
                config = ConfiguracaoChecagem.objects.get(ativo=ativo)

                cotacao_data = yf.Ticker(f"{ativo.ticker}.SA").history(period="1d")
                if cotacao_data.empty:
                    print(f"Não foi possível obter a cotação de {ativo.ticker}")
                    continue
                # Verifica se a cotação foi obtida corretamente
                cotacao_atual = cotacao_data['Close'].iloc[-1]
                print(f'Ativo {ativo.ticker} - Cotação atual: {cotacao_atual:.2f}')

                if cotacao_atual < float(tunel.preco_min):
                    print(f'ALERTA: {ativo.ticker} abaixo do limite mínimo ({tunel.preco_min})')
                    send_mail(
                        subject=f'Alerta: {ativo.ticker} abaixo do mínimo',
                        message=f'O ativo {ativo.ticker} está com cotação {cotacao_atual:.2f}, abaixo de {tunel.preco_min}.',
                        from_email=None,
                        recipient_list=['thiconca@gmail.com'],
                        fail_silently=False,
                    )

                elif cotacao_atual > float(tunel.preco_max):
                    print(f'ALERTA: {ativo.ticker} acima do limite máximo ({tunel.preco_max})')
                    send_mail(
                        subject=f'Alerta: {ativo.ticker} acima do máximo',
                        message=f'O ativo {ativo.ticker} está com cotação {cotacao_atual:.2f}, acima de {tunel.preco_max}.',
                        from_email=None,
                        recipient_list=['thiconca@gmail.com'],
                        fail_silently=False,
                    )
                else:
                    print(f'{ativo.ticker} dentro do túnel')

            except TunelDePreco.DoesNotExist:
                print(f'Túnel de preço não configurado para {ativo.ticker}')
            except ConfiguracaoChecagem.DoesNotExist:
                print(f'Configuração de checagem não encontrada para {ativo.ticker}')
