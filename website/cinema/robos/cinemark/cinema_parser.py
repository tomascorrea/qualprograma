# coding: utf-8
import logging
import re
import urllib2
import BeautifulSoup
from decimal import Decimal

TIPOS_DE_PRECO = [u'Cinemark 3D', u'Matinê', u'Inteira']
"""
Configuração de preço
Preço especial para 3d: se o filme for 3d aplica-se esta regra
preço promocional: aplicado para filmes que não são 3d
sessão desconto: horário e dia definidos. Todas as salas? 3d também? Se o filme começa neste horário vale este preço? Ignorando por hora.
tratar feriados: bosta! ou levanta todos ou @$#%@#$%$%$%$%! colocamos os preços incluindo exceto feriados ou algo assim.
"""

logger = logging.getLogger('qualprograma.robos')

class CinemaParser(BeautifulSoup.BeautifulSoup):
    """
    * <h4>Av. Dr. Chucri Zaidan, 920 - Vila Cordeiro
            Fone: (011) 3048-7400</h4>
    * A cidade está na url sem informação de estado.
    
    """
    def __init__(self, *args, **kwargs):
        kwargs['convertEntities']=BeautifulSoup.BeautifulSoup.HTML_ENTITIES
        super(CinemaParser, self).__init__(*args, **kwargs)

    def cinema(self):
        #TODO achar cidade - <nome> - <cidade>
        
        return {'endereco': self.endereco,
                'telefone': self.telefone,
                'precos': self.precos}

    @property
    def nome(self):
        return self.find('h3').string

    def endereco_telefone(self):
        return self.find('div', id='endereco').find('h4').string

    @property
    def endereco(self):
        try:
            return self.endereco_telefone().split('\n')[0].strip()
        except IndexError:
            logger.ERROR(u'Não consegui extrair endereco de {0}'.format(self.endereco_telefone()))
            return ''

    @property
    def telefone(self):
        res = {'codigo_de_area':'', 'numero':''}
        endereco_telefone = self.endereco_telefone()
        if 'Fone:' in endereco_telefone:
            try:
                bloco_telefone = endereco_telefone.split('Fone :')[1].strip()
            except IndexError:
                logger.ERROR(u'Não consegui extrair código de área de {0}'.format(endereco_telefone))
                return {'codigo_de_area':'', 'numero':''}
            try:
                res['codigo_de_area'] = bloco_telefone.split(' ')[0].strip('(').strip(')')
            except IndexError:
                logger.ERROR(u'Não consegui extrair código de área de {0}'.format(endereco_telefone))
                return {'codigo_de_area':'', 'numero':''}
            try:
                res['numero'] = bloco_telefone.split(' ')[1].strip()
            except IndexError:
                logger.ERROR(u'Não consegui extrair número de {0}'.format(endereco_telefone))
                return {'codigo_de_area':'', 'numero':''}
        else:
            import ipdb;ipdb.set_trace()
            logger.warning(u'Não encontrei telefone em {0}'.format(endereco_telefone))
        return res

    def ignorar(self, valor):
        if isinstance(valor, BeautifulSoup.Tag):
            return not valor.string
        if isinstance(valor, unicode):
            #TODO ignorar sessão desconto?
            return not valor.strip() or u'sessão desconto' in valor.strip().lower()

        return False
 
    def is_tipo_preco(self, valor):
        if isinstance(valor, BeautifulSoup.Tag):
            return valor.string in TIPOS_DE_PRECO

    def is_configuracao_de_matine(self, valor):
        if isinstance(valor, unicode):
            if valor.strip().lower().startswith(u'matinê'):
                return True

    def is_tipo_de_pagamento(self, valor):
        if isinstance(valor, BeautifulSoup.BeautifulSoup):
            return valor.name == 'strong'

    def horario_limite_matine(self, valor):
        return valor.split(' ')[-1].strip('.h')

    def is_preco(self, valor):
        return 'R$' in valor

    def parse_dia(self, valor):
        #usando isoweekday. segunda = 1
        valor = valor.strip().lower()
        if not valor:
            raise ValueError("Can't parse empty day")
        if u'feriado' in valor:
            return u'Feriados'
        first = valor[:1]
        if first.isdigit():
            return unicode(int(first) - 1)
        if u'sáb' in valor or u'sab' in valor:
            return '6'
        if u'dom' in valor:
            return '7'

    def parse_precos_e_condicoes(self, valor):
        preco_pattern = re.compile('r\$ ?(\d+(,\d+)?)')
        valor = valor.strip().lower()
        if 'o dia todo' in valor:
            horario = 'todos'
            preco_match = preco_pattern.search(valor)
            if preco_match:
                preco = Decimal(preco_match.groups()[0].replace(',','.'))
                return [{'preco':preco, 'matine':False}]
        precos = [i.strip() for i in valor.split('-')]
        res = []
        for preco_str in precos:
            matine = False
            if u'matinê' in precos:
                matine = True
            preco_match = preco_pattern.search(valor)
            if preco_match:
                preco = Decimal(preco_match.groups()[0].replace(',','.'))
                res.append({'preco': preco, 'matine':matine})
        return res

    def precos_por_dia(self, valor):
        """
        4ª: R$ 12,00 o dia todo
        2ª,3ª e 5ª: R$ 13,00 (matinê) - R$ 15,00 (noite)
        6ª,Sab.,Dom. e Feriados: R$ 15,00 (matinê) - R$ 19,00 (noite)
        """
        try:
            dias, precos = valor.strip().split(':')
        except ValueError:
            logger.error(u'Não consegui extrair preços e dias de {0}'.format(unicode(valor)))
            return []
        dias = dias.replace(' e ',',').split(',')
        dias = [self.parse_dia(dia) for dia in dias if dia]
        precos = self.parse_precos_e_condicoes(precos)
        res = []
        for dia in dias:
            for preco in precos:
                res.append({'dia':dia, 'valor':preco})
        return res

    @property
    def precos(self):
        contents = self.find('div', id='precos').find('p').contents
        res = {}
        tipo_atual = 'desconhecido'
        res[tipo_atual] = []
        for content in contents:
            if self.ignorar(content):
                continue
            if self.is_tipo_preco(content):
                tipo_atual = content.string
                res[content.string] = []
                continue
            if self.is_configuracao_de_matine(content):
                res['ultima_sessao_matine'] = self.horario_limite_matine(content) 
                continue
            if self.is_tipo_de_pagamento(content):
                res['tipo_de_pagamento'] = content.string
                continue
            if self.is_preco(content):
                res[tipo_atual] = self.precos_por_dia(content)
        return res
 
    @property
    def salas(self):
        #TODO descobrir salas especiais como bradesco prime
        return []

