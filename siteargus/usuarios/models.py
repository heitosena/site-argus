from django.db import models

# Create your models here.
# 
class usuario(models.Model):
    nome = models.CharField(max_length=120)
    email = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20)
    senha = models.CharField(max_length=255)