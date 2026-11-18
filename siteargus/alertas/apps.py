from django.apps import AppConfig


class AlertasConfig(AppConfig):
    name = 'alertas'

    def ready(self):
        import os

        if os.environ.get('RUN_MAIN') == 'true':
            from .scheduler import iniciar_agendador
            iniciar_agendador()
