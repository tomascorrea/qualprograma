# -*- coding: utf-8 -*-
import logging
from django.core.management.base import NoArgsCommand
from cinema.robos.cinemark.crawler import CinemaCrawler
from cinema.models import Cinema, ConfiguracaoPreco
from endereco.models import Telefone, Endereco

logger = logging.getLogger('qualprograma.robos')

class Command(NoArgsCommand):
    
    def handle(self, *args, **options):
        ConfiguracaoPreco.objects.all().delete()
        Cinema.objects.all().delete()
        for nome, url, rede, dados in CinemaCrawler().get_cinemas():
            try:
                cinema = Cinema.objects.get(rede = rede, nome=nome)
            except Cinema.DoesNotExist:
                cinema = None
            if not cinema:    
                if dados['endereco']:
                    endereco = Endereco.objects.create(endereco=dados['endereco'])
                cinema = Cinema.objects.create(rede = rede, nome=nome, endereco=endereco, url=url)
                if dados['telefone']:
                    telefone = Telefone.objects.create(codigo_de_area = dados['telefone']['codigo_de_area'], 
                                                       numero = dados['telefone']['numero'])
                    cinema.telefones.add(telefone)

            for key, valor in dados['precos'].items():
                if key == 'ultima_sessao_matine':
                    try:
                        ultima_sessao_matine = valor
                    except ValueError:
                        logger.error(u'Erro ao gravar hora da matine. Valor inválido:{0}'.format(int(valor)))
                continue
                configuracao_preco = ConfiguracaoPreco.objects.create(cinema=cinema)
                if key == 'Cinemark 3D':
                    configuracao_preco.tipo_do_filme = '3D'
                #TODO:tratar sala bradesco prime
                for item in valor:
                    configuracao_preco.dia_da_semana = item['dia']
                    configuracao_preco.matine['valor']['matine']
                    configuracao_preco.valor['valor']['preco']
                configuracao_preco.save()
            cinema.save()
                        
