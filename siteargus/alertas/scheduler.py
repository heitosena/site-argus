
import threading
import time

from django.db import close_old_connections


def iniciar_agendador():
    def executar():
        while True:
            time.sleep(180)

            try:
                from .services import processar_alertas

                close_old_connections()
                processar_alertas()

                print("Processamento automático de alertas executado com sucesso.")

            except Exception as erro:
                print(f"Erro ao processar alertas automaticamente: {erro}")

            finally:
                close_old_connections()

    thread = threading.Thread(
        target=executar,
        daemon=True
    )
    thread.start()
