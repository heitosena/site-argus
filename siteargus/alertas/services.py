
import logging

from django.db import transaction
from django.utils import timezone

from sensores.models import Dispositivo, Registro
from usuarios.models import Usuario
from notificacoes.services import enviar_alerta_n8n
from .models import Alerta, ProcessamentoAlerta


logger = logging.getLogger(__name__)


def resolver_queryset(alertas):
    """
    Resolve os alertas informados e registra a data da resolução.
    """

    alertas.update(
        status='resolvido',
        data_resolucao=timezone.now()
    )


def atualizar_alerta(dispositivo, tipo, descricao):
    """
    Mantém apenas um alerta ativo para a condição atual.
    Resolve o alerta anterior quando a condição muda.
    """

    alertas_ativos = Alerta.objects.filter(
        dispositivo=dispositivo,
        status='ativo'
    )

    alerta_existente = alertas_ativos.filter(
        tipo=tipo
    ).first()

    if alerta_existente:
        # Resolve possíveis alertas ativos de outros tipos.
        resolver_queryset(
            alertas_ativos.exclude(id=alerta_existente.id)
        )
        return alerta_existente, False

    # Resolve o alerta anterior.
    resolver_queryset(alertas_ativos)

    # Cria o novo alerta.
    alerta = Alerta.objects.create(
        dispositivo=dispositivo,
        tipo=tipo,
        descricao=descricao
    )

    return alerta, True


def resolver_alertas(dispositivo, tipo=None):
    """
    Resolve os alertas ativos de um dispositivo.
    Se um tipo for informado, resolve somente aquele tipo.
    """

    alertas = Alerta.objects.filter(
        dispositivo=dispositivo,
        status='ativo'
    )

    if tipo:
        alertas = alertas.filter(tipo=tipo)

    resolver_queryset(alertas)


def enviar_alerta_pendente(alerta_id, dados):
    """
    Envia um alerta ao n8n e marca como enviado
    somente quando a comunicação for bem-sucedida.
    """

    alerta = Alerta.objects.filter(
        id=alerta_id,
        status='ativo',
        n8n_enviado=False
    ).first()

    if not alerta:
        return

    try:
        enviado = enviar_alerta_n8n(dados)

        if enviado:
            Alerta.objects.filter(
                id=alerta.id,
                n8n_enviado=False
            ).update(n8n_enviado=True)

            logger.info(
                'Notificação do alerta %s enviada ao n8n.',
                alerta.id
            )

    except Exception:
        logger.exception(
            'Erro ao enviar o alerta %s ao n8n.',
            alerta.id
        )


@transaction.atomic
def processar_nova_leitura(registro):
    """
    Processa imediatamente uma nova leitura recebida pela API.
    Cria alertas quando a condição muda e envia notificações ao n8n.
    """

    dispositivo = registro.dispositivo

    # Verifica se o dispositivo está inativo.
    if dispositivo.status == 'Inativo':
        alerta, criado = atualizar_alerta(
            dispositivo,
            'inativo',
            'O dispositivo está inativo.'
        )

    else:
        # Resolve o alerta de inatividade quando necessário.
        resolver_alertas(dispositivo, tipo='inativo')

        # Identifica a condição atual do gás.
        if registro.vazamento:
            alerta, criado = atualizar_alerta(
                dispositivo,
                'vazamento',
                'Perigo de vazamento de gás detectado!'
            )

        elif registro.gas_percentual > 45:
            alerta, criado = atualizar_alerta(
                dispositivo,
                'perigo',
                'Perigo de vazamento! Nível de gás acima de 45%.'
            )

        elif registro.gas_percentual > 20:
            alerta, criado = atualizar_alerta(
                dispositivo,
                'atencao',
                'Nível de gás elevado. Atenção necessária.'
            )

        else:
            resolver_alertas(dispositivo)
            return

    # Busca o usuário responsável pelo dispositivo.
    if alerta and not alerta.n8n_enviado:

        usuario = Usuario.objects.filter(
            id=dispositivo.usuario_id
        ).first()

        if not usuario or not usuario.email:
            logger.warning(
                'Dispositivo %s não possui usuário ou e-mail cadastrado.',
                dispositivo.id
            )
            return

        # Prepara os dados para o n8n.
        dados = {
            'dispositivo': dispositivo.nome,
            'gas_percentual': registro.gas_percentual,
            'nivel_gas': registro.nivel_gas,
            'vazamento': registro.vazamento,
            'mensagem': alerta.descricao,
            'email': usuario.email
        }

        # Aguarda a confirmação da transação antes de enviar.
        transaction.on_commit(
            lambda alerta_id=alerta.id, payload=dados:
                enviar_alerta_pendente(alerta_id, payload)
        )


@transaction.atomic
def processar_alertas():
    """
    Processa as novas leituras de todos os dispositivos.
    Leituras antigas são ignoradas na primeira execução.
    """

    dispositivos = Dispositivo.objects.all()

    for dispositivo in dispositivos:

        # Verifica se o dispositivo está inativo.
        if dispositivo.status == 'Inativo':
            atualizar_alerta(
                dispositivo,
                'inativo',
                'O dispositivo está inativo.'
            )
        else:
            # Resolve o alerta de inatividade quando necessário.
            resolver_alertas(dispositivo, tipo='inativo')

        # Recupera o controle de processamento.
        processamento, criado = (
            ProcessamentoAlerta.objects.select_for_update()
            .get_or_create(dispositivo=dispositivo)
        )

        # Na primeira execução, ignora as leituras antigas.
        if criado:
            ultimo_registro = Registro.objects.filter(
                dispositivo=dispositivo
            ).order_by('-id').first()

            if ultimo_registro:
                processamento.ultimo_registro_id = ultimo_registro.id
                processamento.save(
                    update_fields=['ultimo_registro_id', 'atualizado_em']
                )

            continue

        # Busca somente registros ainda não processados.
        registros = Registro.objects.filter(
            dispositivo=dispositivo,
            id__gt=processamento.ultimo_registro_id
        ).order_by('id')

        for registro in registros:

            # Dispositivo inativo não gera alertas de nível de gás.
            if dispositivo.status == 'Inativo':
                processamento.ultimo_registro_id = registro.id
                processamento.save(
                    update_fields=['ultimo_registro_id', 'atualizado_em']
                )
                continue

            # Vazamento detectado tem prioridade.
            if registro.vazamento:
                atualizar_alerta(
                    dispositivo,
                    'vazamento',
                    'Perigo de vazamento de gás detectado!'
                )

            # Acima de 45%: Perigo de vazamento.
            elif registro.gas_percentual > 45:
                atualizar_alerta(
                    dispositivo,
                    'perigo',
                    'Perigo de vazamento! Nível de gás acima de 45%.'
                )

            # Acima de 20% até 45%: Atenção.
            elif registro.gas_percentual > 20:
                atualizar_alerta(
                    dispositivo,
                    'atencao',
                    'Nível de gás elevado. Atenção necessária.'
                )

            # Até 20%: Normal.
            else:
                resolver_alertas(dispositivo)

            # Atualiza o último registro processado.
            processamento.ultimo_registro_id = registro.id
            processamento.save(
                update_fields=['ultimo_registro_id', 'atualizado_em']
            )
