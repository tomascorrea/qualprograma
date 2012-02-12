# coding: utf-8
from django.test import TestCase
from cinema.robos.cinemark.cinema import  CinemaParser

class TestCinemaParser(TestCase):
    def setUp(self):
	self.parser = CinemaParser()

    def test_telefone_vazio(self):
        self.parser.endereco_telefone = lambda : u'Rua Izabel Redentora, N\xba 1434 Loja 206 S\xe3o Jos\xe9 dos Pinhais PR\n\t\t\tFone: '
        tel = self.parser.telefone
        self.assertEqual(tel['codigo_de_area'],'')
        self.assertEqual(tel['numero'],'')
	
	
