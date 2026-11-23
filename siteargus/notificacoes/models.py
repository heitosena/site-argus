from django.db import models

# Create your models here.


# Armazena os contatos adicionais utilizados para receber notificações.
class ContatoNotificacao(models.Model):

    TIPO_CONTATO = [
        ('email', 'E-mail'),
        ('telefone', 'Telefone'),
    ]

    id = models.AutoField(primary_key=True)

    usuario_id = models.IntegerField()

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CONTATO
    )

    valor = models.CharField(max_length=150)

    ativo = models.BooleanField(default=True)

    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contatos_notificacao'
        ordering = ['-data_criacao']

    def __str__(self):
        return f'{self.tipo}: {self.valor}'


# =========================================
# CANAIS DE NOTIFICAÇÃO
# =========================================

class CanalNotificacao(models.Model):

    TIPOS_CANAL = [
        ('email', 'E-mail'),
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
    ]

    id = models.AutoField(primary_key=True)
    usuario_id = models.IntegerField()
    tipo = models.CharField(max_length=20, choices=TIPOS_CANAL)
    identificador = models.CharField(max_length=150)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'canais_notificacao'
        ordering = ['-data_criacao']

    def __str__(self):
        return f'{self.tipo}: {self.identificador}'


# =========================================
# HISTÓRICO DE NOTIFICAÇÕES
# =========================================

class HistoricoNotificacao(models.Model):

    STATUS_NOTIFICACAO = [
        ('pendente', 'Pendente'),
        ('enviada', 'Enviada'),
        ('falhou', 'Falhou'),
    ]

    id = models.AutoField(primary_key=True)
    usuario_id = models.IntegerField()

    canal = models.ForeignKey(
        CanalNotificacao,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='historico'
    )

    tipo_alerta = models.CharField(max_length=50)
    mensagem = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_NOTIFICACAO,
        default='pendente'
    )

    erro = models.TextField(blank=True, null=True)

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_envio = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'historico_notificacoes'
        ordering = ['-data_criacao']

    def __str__(self):
        return f'Notificação {self.id} - {self.status}'
