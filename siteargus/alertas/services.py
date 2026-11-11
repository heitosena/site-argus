from django.db import transaction
from django.utils import timezone

from sensores.models import Dispositivo, Registro
from .models import Alerta, ProcessamentoAlerta


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
        return

    # Resolve o alerta anterior.
    resolver_queryset(alertas_ativos)

    # Cria o novo alerta.
    Alerta.objects.create(
        dispositivo=dispositivo,
        tipo=tipo,
        descricao=descricao
    )


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

            # Vazamento tem prioridade.
            if registro.vazamento:
                atualizar_alerta(
                    dispositivo,
                    'vazamento',
                    'Vazamento de gás detectado!'
                )

            elif registro.nivel_gas == 'Perigo':
                atualizar_alerta(
                    dispositivo,
                    'perigo',
                    'Nível de gás em estado de perigo.'
                )

            elif registro.nivel_gas == 'Atenção':
                atualizar_alerta(
                    dispositivo,
                    'atencao',
                    'Nível de gás acima do normal. Atenção necessária.'
                )

            elif registro.nivel_gas == 'Normal':
                resolver_alertas(dispositivo)

            # Atualiza o último registro processado.
            processamento.ultimo_registro_id = registro.id
            processamento.save(
                update_fields=['ultimo_registro_id', 'atualizado_em']
            )
