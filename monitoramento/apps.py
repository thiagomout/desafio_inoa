from django.apps import AppConfig


class MonitoramentoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoramento'

    def ready(self):
        from django_q.models import Schedule
        from django.db.utils import OperationalError, ProgrammingError

        try:
            if not Schedule.objects.filter(func='monitoramento.tasks.checar_cotacoes').exists():
                Schedule.objects.create(
                    name='Checagem de Cotações',
                    func='monitoramento.tasks.checar_cotacoes',
                    schedule_type=Schedule.MINUTES,
                    minutes=1  # Roda a cada 1 minuto
                )
        except (OperationalError, ProgrammingError):
            pass