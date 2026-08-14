from django.db import models

class Dispositivo(models.Model):
    # Nome dado ao dispositivo, por exemplo: "sensor Cozinha"
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
            ('Ativo, Ativo'),
            ('Inativo, Inativo')
            ('Manutenção, Manutenção'),
        ],
        default='Ativo'
    )
# Data e hora da última comunicação do ESP32
# Pode ficar vazio enquanto o dispositivo ainda não se comunicou 
ultima_comunicacao = models.DateTimeField(
    null=True
    blank=True
)
