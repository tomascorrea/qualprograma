import os

from django.test import TestCase
from django.conf import settings
from django.core.management import call_command

from cinema.models import Filme

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

settings.HAYSTACK_WHOOSH_PATH = '%s/search_index' % CURRENT_DIR
import shutil

class FilmeBuscaTest(TestCase):

    def setUp(self):
        call_command("clear_index", verbosity=0, interactive=False)

    def tearDown(self):
        pass

    def test_filme_eh_encontrado_na_busca(self):
        filme = Filme()
        filme.titulo = "Nome do filme"
        filme.save()

        response = self.client.get("/busca/?q=nome")
        self.assertTrue("Nome do filme" in response.content)

    def test_filme_nao_deve_ser_encontrado_na_busca(self):
        filme = Filme()
        filme.titulo = "Nome do filme"
        filme.save()

        response = self.client.get("/busca/?q=nomeeee")
        self.assertTrue("Nome do filme" not in response.content)


