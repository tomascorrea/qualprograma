import datetime
from haystack.indexes import *
from haystack import site
from cinema.models import Filme


class FilmeIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    titulo = CharField(model_attr='titulo')

site.register(Filme, FilmeIndex)