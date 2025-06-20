from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import Ativo, TunelDePreco
import yfinance as yf

def checar_cotacoes():
    agora = timezone.now()
    ativos = Ativo.objects.all()

    for ativo in ativos:
        # Respeitar intervalo de checagem
        if ativo.ultima_checagem:
            proxima_checagem = ativo.ultima_checagem + timedelta(minutes=ativo.intervalo_checagem)
            if agora < proxima_checagem:
                continue

        try:
            tunel = TunelDePreco.objects.get(ativo=ativo)
        except TunelDePreco.DoesNotExist:
            continue

        try:
            cotacao_data = yf.Ticker(f"{ativo.ticker}.SA").history(period="1d")
            if cotacao_data.empty:
                continue

            preco_atual = cotacao_data['Close'].iloc[-1]
            estado_atual = ativo.estado
            user_email = ativo.user.email

            if preco_atual < float(tunel.preco_min) and estado_atual != -1:
                if user_email:
                    send_mail(
                        subject=f"Alerta: {ativo.ticker} abaixo do mínimo",
                        message=f"O ativo {ativo.ticker} está com cotação {preco_atual:.2f}, abaixo de {tunel.preco_min}. Recomenda-se comprar.",
                        from_email=None,
                        recipient_list=[user_email],
                        fail_silently=False,
                    )
                ativo.estado = -1

            elif preco_atual > float(tunel.preco_max) and estado_atual != 1:
                if user_email:
                    send_mail(
                        subject=f"Alerta: {ativo.ticker} acima do máximo",
                        message=f"O ativo {ativo.ticker} está com cotação {preco_atual:.2f}, acima de {tunel.preco_max}. Recomenda-se vender.",
                        from_email=None,
                        recipient_list=[user_email],
                        fail_silently=False,
                    )
                ativo.estado = 1

            elif float(tunel.preco_min) <= preco_atual <= float(tunel.preco_max) and estado_atual != 0:
                if user_email:
                    send_mail(
                        subject=f"Alerta: {ativo.ticker} voltou ao túnel",
                        message=f"O ativo {ativo.ticker} está com cotação {preco_atual:.2f}, dentro do intervalo definido.",
                        from_email=None,
                        recipient_list=[user_email],
                        fail_silently=False,
                    )
                ativo.estado = 0

            ativo.ultima_checagem = agora
            ativo.save()

        except Exception as e:
            print(f"Erro ao processar {ativo.ticker}: {e}")
