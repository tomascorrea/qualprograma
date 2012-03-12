# coding: utf-8

from django.db import models
from endereco.models import Endereco, Telefone

# Create your models here.
from django.utils.translation import ugettext_lazy as _


class Rede(models.Model):
    nome = models.CharField(_(u"Nome"), max_length=200)
    url = models.CharField(_(u"url"), max_length=200)

    def __unicode__(self):
        return self.nome


class Cinema(models.Model):
    rede = models.ForeignKey(Rede)
    nome = models.CharField(_(u"Nome"), max_length=100)
    url = models.CharField(_(u"url"), max_length=200)
    endereco = models.OneToOneField(Endereco)
    telefones = models.ManyToManyField(Telefone)
    formas_de_pagamento = models.CharField(_(u"Formas de Pagamento"), null=True, max_length=200)
    ultima_sessao_matine = models.TimeField(null=True)

    def __unicode__(self):
        return u':'.join([self.rede.nome, self.nome])

HUMAN_DAYS = {1:'2a', 2: '3a', 3:'4a', 4:'5a', 5:'6a', '6':'sáb', 7:'dom'}
class ConfiguracaoPreco(models.Model):
    cinema = models.ForeignKey(Cinema)
    valor = models.DecimalField(_(u"Preço"), max_digits=5, decimal_places=2)
    dia_da_semana = models.IntegerField() #0 é igual a todos, 1 é 2a (isoweekay)
    hora = models.TimeField(null=True) #null vale para todos os horários
    tipo_da_sala = models.CharField(max_length=100, default="normal")
    tipo_do_filme = models.CharField(max_length=100, default="normal") #3D
    matine = models.BooleanField(default=False)


class Sala(models.Model):
    cinema = models.ForeignKey(Cinema)
    nome = models.CharField(_(u"Título"), max_length=200)
    tipo = models.CharField(max_length=100, default='normal') #para salas tipo bradesco prime


class Filme(models.Model):
    titulo = models.CharField(_(u"Título"), max_length=200)
    sinopse = models.TextField(_(u"Sinopse"))
    lancamento = models.BooleanField(_(u"Lançamento"), default=False)
    categorias = models.CharField(max_length=200) #TODO: classe ou tag?
    url = models.CharField(_(u"url"), max_length=200)

    def __unicode__(self):
        return self.titulo

class Temporada(models.Model):
    sala = models.ForeignKey(Sala)
    filme = models.ForeignKey(Filme)
    inicio = models.DateField(_(u"Início"))
    fim = models.DateField(_(u"Fim"))


class Horario(models.Model):
    temporada = models.ForeignKey(Temporada)
    inicio = models.CharField(_(u"Início"), max_length="5")
    preco = models.DecimalField(_(u"Preço"), max_digits=5, decimal_places=2)
    dublado = models.BooleanField(_(u"Dublado"), default=False)
    

class Sessao(models.Model):
    """Modelo desnormalizado para facilitar indexações e buscas.
    É gerenciado pelas Temporadas e horários. Quaisquer alterações nelas "criam" ou "apagam" sessões.
    """
    rede = models.ForeignKey(Rede)
    cinema = models.ForeignKey(Cinema)
    sala = models.ForeignKey(Sala)
    filme = models.ForeignKey(Filme)
    inicio = models.DateTimeField(_(u"Início"))
    preco = models.DecimalField(_(u"Preço"), max_digits=5, decimal_places=2)
    dublado = models.BooleanField(_(u"Dublado"), default=False)
    legendado = models.BooleanField(_(u"Legendado"), default=False)
    promocao = models.BooleanField(_(u"Promoção"), default=False)
    tres_d = models.BooleanField(_(u"3D"), default=False)
    estreia = models.BooleanField(_(u"Estréia"), default=False)
    materna = models.BooleanField(_(u"Materna"), default=False)

    class Meta:
        verbose_name_plural = _(u"Sessões")







