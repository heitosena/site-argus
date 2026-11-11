from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Dispositivo(models.Model):

    # Identificador do dispositivo (compatível com o banco MySQL)
    id = models.AutoField(primary_key=True)

    # Nome dado ao dispositivo
    nome = models.CharField(max_length=100)

    # Modelo do dispositivo ESP32
    modelo = models.CharField(
        max_length=50,
        default='ESP32 - Sensor de Gás'
    )

    # Situação atual do dispositivo
    status = models.CharField(
        max_length=20,
        choices=[
            ('Ativo', 'Ativo'),
            ('Inativo', 'Inativo'),
            ('Manutenção', 'Manutenção'),
        ],
        default='Ativo'
    )

    # Data e hora da última comunicação
    ultima_comunicacao = models.DateTimeField(
        null=True,
        blank=True
    )

    # Porcentagem da bateria
    bateria = models.PositiveIntegerField(
        default=100,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    # Indica se o ESP32 está conectado à rede
    rede_conectada = models.BooleanField(default=False)

    # Identificador do usuário responsável pelo dispositivo
    usuario_id = models.IntegerField(default=1)

    class Meta:
        db_table = 'dispositivos'

    def __str__(self):
        return self.nome


class Localizacao(models.Model):
    # Tipo do local onde o dispositivo está instalado
    instituicao = models.CharField(
        max_length=20,
        choices=[
            ('Casa', 'Casa'),
            ('Apartamento', 'Apartamento'),
            ('Empresa', 'Empresa'),
            ('Comércio', 'Comércio'),
        ]
    )

    # Descrição do local
    # Exemplo: "Cozinha principal"
    descricao = models.CharField(max_length=150)

    # Endereço onde o dispositivo está instalado
    endereco = models.CharField(max_length=200)

    # Dispositivo relacionado a esta localização
    dispositivo = models.OneToOneField(
        Dispositivo,
        on_delete=models.CASCADE,
        related_name='localizacao'
    )

    class Meta:
        db_table = 'localizacao'

    def __str__(self):
        return self.descricao


class Registro(models.Model):
    # Data e hora em que o registro foi recebido
    data_hora = models.DateTimeField(auto_now_add=True)

    # Temperatura do ambiente em graus Celsius
    temperatura = models.DecimalField(
        max_digits=5,
        decimal_places=1
    )

    # Umidade do ambiente em porcentagem
    umidade = models.DecimalField(
        max_digits=5,
        decimal_places=1
    )

    # Porcentagem de gás detectada pelo ESP32
    gas_percentual = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    # Classificação do nível de gás
    nivel_gas = models.CharField(
        max_length=10,
        choices=[
            ('Normal', 'Normal'),
            ('Atenção', 'Atenção'),
            ('Perigo', 'Perigo'),
            ('Inativo', 'Inativo'),
        ]
    )

    # Indica se foi detectado vazamento
    vazamento = models.BooleanField()

    # Indica se o usuário decidiu salvar este registro
    salvo = models.BooleanField(default=False)

    # Dispositivo responsável por enviar este registro
    dispositivo = models.ForeignKey(
        Dispositivo,
        on_delete=models.CASCADE,
        related_name='registros'
    )

    class Meta:
        db_table = 'registros'

    def __str__(self):
        return f"{self.dispositivo.nome} - {self.data_hora}"


class LeituraSalva(models.Model):
    # Data e hora da leitura original
    data_hora = models.DateTimeField()

    # Dados ambientais registrados
    temperatura = models.DecimalField(
        max_digits=5,
        decimal_places=1
    )

    umidade = models.DecimalField(
        max_digits=5,
        decimal_places=1
    )

    gas_percentual = models.PositiveIntegerField()

    # Classificação do nível de gás
    nivel_gas = models.CharField(max_length=10)

    # Indica se houve vazamento
    vazamento = models.BooleanField()

    # Nome do dispositivo no momento em que a leitura foi salva
    dispositivo_nome = models.CharField(max_length=100)

    # Data em que o usuário salvou a leitura
    data_salvamento = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'leituras_salvas'
        ordering = ['-data_hora']

    def __str__(self):
        return f"{self.dispositivo_nome} - {self.data_hora}"