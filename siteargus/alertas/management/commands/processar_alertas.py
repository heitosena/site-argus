
from django.core.management.base import BaseCommand
from alertas.services import processar_alertas


class Command(BaseCommand):
    help = 'Processa novas leituras e atualiza os alertas dos dispositivos.'

    def handle(self, *args, **options):
        try:
            processar_alertas()

            self.stdout.write(
                self.style.SUCCESS(
                    'Processamento de alertas executado com sucesso.'
                )
            )

        except Exception as erro:
            self.stderr.write(
                self.style.ERROR(
                    f'Erro ao processar alertas: {erro}'
                )
            )
            raise
