
import logging
import requests

from django.conf import settings

logger = logging.getLogger(__name__)


def enviar_alerta_n8n(dados):
    """
    Envia os dados de um alerta do A.R.G.U.S. para o Webhook do n8n.
    """

    webhook_url = getattr(settings, 'N8N_WEBHOOK_URL', None)

    if not webhook_url:
        logger.error('URL do Webhook do n8n não configurada.')
        return False

    try:
        resposta = requests.post(
            webhook_url,
            json=dados,
            timeout=5
        )

        resposta.raise_for_status()

        logger.info('Alerta enviado ao n8n com sucesso.')

        return True

    except requests.RequestException as erro:
        logger.error(
            'Falha ao enviar alerta para o n8n: %s',
            erro
        )

        return False
