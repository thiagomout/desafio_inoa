from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from monitoramento.models import Ativo, TunelDePreco
import yfinance as yf

class Command(BaseCommand):
    help = 'Checa cotações dos ativos por usuário e envia alertas por e-mail.'

    def handle(self, *args, **kwargs):
        agora = timezone.now()
        ativos = Ativo.objects.all()

        for ativo in ativos:
            try:
                intervalo = ativo.intervalo_checagem
                tunel = TunelDePreco.objects.get(ativo=ativo)
            except (intervalo.DoesNotExist, TunelDePreco.DoesNotExist):
                print(f"[{ativo.ticker}] Sem configuração ou túnel de preço. Pulando...")
                continue

            # Verificar intervalo de checagem
            if ativo.ultima_checagem:
                proxima_checagem = ativo.ultima_checagem + timedelta(minutes=intervalo)
                if agora < proxima_checagem:
                    continue  # Ainda não é hora de checar

            try:
                cotacao_data = yf.Ticker(f"{ativo.ticker}.SA").history(period="1d")
                if cotacao_data.empty:
                    print(f"Não foi possível obter a cotação de {ativo.ticker}")
                    continue

                preco_atual = cotacao_data['Close'].iloc[-1]
                print(f"[{ativo.ticker}] Cotação atual: {preco_atual:.2f}")

                user_email = ativo.user.email
                estado_atual = ativo.estado

                if preco_atual < float(tunel.preco_min):
                    if estado_atual != -1:
                        print(f"[{ativo.ticker}] ALERTA: Abaixo do mínimo ({tunel.preco_min})")
                        if user_email:
                            send_mail(
                                subject=f"Alerta: {ativo.ticker} abaixo do mínimo",
                                message=f"O ativo {ativo.ticker} está com cotação {preco_atual:.2f}, abaixo de {tunel.preco_min}.",
                                from_email=None,
                                recipient_list=[user_email],
                            )
                        ativo.estado = -1

                elif preco_atual > float(tunel.preco_max):
                    if estado_atual != 1:
                        print(f"[{ativo.ticker}] ALERTA: Acima do máximo ({tunel.preco_max})")
                        if user_email:
                            send_mail(
                                subject=f"Alerta: {ativo.ticker} acima do máximo",
                                message=f"O ativo {ativo.ticker} está com cotação {preco_atual:.2f}, acima de {tunel.preco_max}.",
                                from_email=None,
                                recipient_list=[user_email],
                            )
                        ativo.estado = 1

                else:
                    if estado_atual != 0:
                        print(f"[{ativo.ticker}] Voltou para dentro do túnel.")
                        if user_email:
                            send_mail(
                                subject=f"Alerta: {ativo.ticker} voltou para o túnel",
                                message=f"O ativo {ativo.ticker} está com cotação {preco_atual:.2f}, dentro do túnel ({tunel.preco_min} - {tunel.preco_max}).",
                                from_email=None,
                                recipient_list=[user_email],
                            )
                        ativo.estado = 0

                # Atualiza ultima checagem e salva o estado novo
                ativo.ultima_checagem = agora
                ativo.save()

            except Exception as e:
                print(f"Erro ao checar {ativo.ticker}: {e}")