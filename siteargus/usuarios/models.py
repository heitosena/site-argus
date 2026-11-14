from django.db import models

# Create your models here.
# 
class Usuario(models.Model):

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=120)
    email = models.EmailField(max_length=150, unique = True)
    telefone = models.CharField(max_length=20)
    senha = models.CharField(max_length=255)

    class Meta:
        db_table = 'usuarios'
        managed = False