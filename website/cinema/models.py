# coding: utf-8

from django.db import models
from endereco.models import Endereco, Telefone

# Create your models here.
from django.utils.translation import ugettext_lazy as _


class Rede(models.Model):
    nome = models.Charfield(_(u"Nome"), max_lenght=200)
    url = models.Charfield(_(u"url"), max_lenght=200)

class Cinema(models.Model):
    rede = models.ForeignKey(Rede)
    endereco = models.OneToOneField(Endereco)
    telefones = models.ManyToMany(Telefone)

class Filme(models.Model):
    titulo = models.Charfield(_(u"Título"), max_lenght=200)
    sinopse = models.TextField(_(u"Sinopse"))
    lancamento = models.BooleanField(_(u"Lançamento"), default=False)
    url = models.Charfield(_(u"url"), max_lenght=200)


class Temporada(models.Model):
    filme = models.ForeignKey(Filme)
    inicio = models.DateField(_(u"Início"))
    fim = models.DateField(_(u"Fim"))
    

class Sessao(models.Model):
    temporada = models.ForeignKey(Temporada)
    inicio = models.TimeField(_(u"Início"))
    sala = models.Charfield(_(u"Sala"),max_lenght=200)
    preco = models.DecimalField(_(u"Preço"), max_digits=5, decimal_places=2)
    dublado = models.BooleanField(_(u"Dublado"), default=False)

    







