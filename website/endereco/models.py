from django.db import models

# Create your models here.


class Endereco(models.Model):
    endereco = models.TextField()


class Telefone(models.Model):
    codigo_de_area = models.CharField(max_length=2, default="11") 
    numero = models.CharField(max_length=8)


