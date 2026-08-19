from django.db import models


class Dispositivo(models.Model):
    # Nome dado ao dispositivo
    # Exemplo: "Sensor Cozinha"
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

    # Data e hora da última comunicação do ESP32
    # Pode ficar vazio enquanto o dispositivo ainda não se comunicou
    ultima_comunicacao = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        # Mostra o nome do dispositivo
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

    def __str__(self):
        # Mostra a descrição da localização
        return self.descricao


class Registro(models.Model):
    # Data e hora em que o registro foi recebido
    data_hora = models.DateTimeField(auto_now_add=True)

    # Temperatura do ambiente em graus Celsius
    # Exemplo: 28.5
    temperatura = models.DecimalField(
        max_digits=4,
        decimal_places=1
    )

    # Umidade do ambiente em porcentagem
    # Exemplo: 47.1
    umidade = models.DecimalField(
        max_digits=4,
        decimal_places=1
    )

    # Quantidade de gás detectada em PPM
    # O valor é armazenado como número inteiro
    gas_ppm = models.IntegerField()

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

    # Dispositivo responsável por enviar este registro
    # Um dispositivo pode possuir vários registros
    dispositivo = models.ForeignKey(
        Dispositivo,
        on_delete=models.CASCADE,
        related_name='registros'
    )

    def __str__(self):
        # Identifica o registro pelo dispositivo e pela data
        return f"{self.dispositivo.nome} - {self.data_hora}"