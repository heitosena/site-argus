from django.db import models
from sensores.models import Dispositivo


class Alerta(models.Model):

    # Tipos de alerta
    TIPOS_ALERTA = [
        ('atencao', 'Atenção'),
        ('perigo', 'Perigo'),
        ('vazamento', 'Vazamento detectado'),
        ('inativo', 'Dispositivo inativo'),
    ]

    # Situação do alerta
    STATUS_ALERTA = [
        ('ativo', 'Ativo'),
        ('resolvido', 'Resolvido'),
    ]

    dispositivo = models.ForeignKey(
        Dispositivo,
        on_delete=models.CASCADE,
        related_name='alertas'
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_ALERTA
    )

    descricao = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_ALERTA,
        default='ativo'
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True
    )

    data_resolucao = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-data_criacao']

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.dispositivo.nome}'


class ProcessamentoAlerta(models.Model):

    # Dispositivo cujas leituras estão sendo processadas
    dispositivo = models.OneToOneField(
        'sensores.Dispositivo',
        on_delete=models.CASCADE,
        related_name='processamento_alertas'
    )

    # ID da última leitura processada
    ultimo_registro_id = models.PositiveBigIntegerField(
        default=0
    )

    # Data da última atualização do processamento
    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Processamento de alerta'
        verbose_name_plural = 'Processamentos de alertas'

    def __str__(self):
        return f'Processamento - {self.dispositivo.nome}'
