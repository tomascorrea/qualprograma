from django.db import models

# Create your models here.


class Endereco(models.Model):
    endereco = models.TextField()

    def __unicode__(self):
        return unicode(self.endereco)


class Telefone(models.Model):
    codigo_de_area = models.CharField(max_length=2, default="11") 
    numero = models.CharField(max_length=8)

    def __unicode__(self):
        return u'(%codigo_de_area) $(numero)'.format(codigo_de_area=self.codigo_de_area, numero=self.numero)
