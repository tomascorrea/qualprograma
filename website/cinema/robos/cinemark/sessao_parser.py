# coding: utf-8
import logging
import BeautifulSoup
import re
from datetime import time

logger = logging.getLogger('qualprograma.robos')

class SessaoParser(BeautifulSoup.BeautifulSoup):

    def __init__(self, *args, **kwargs):
        kwargs['convertEntities']=BeautifulSoup.BeautifulSoup.HTML_ENTITIES
        super(SessaoParser, self).__init__(*args, **kwargs)

    def get_sessao_bloco(self):
        return self.findAll('div', {'class':'filme'})

    def aplica_regras_de_datas(self, span_sala, intervalo):
        span_regra = span_sala.findNextSibling('span', {'class':'letra-legenda'})
        if span_regra:
            regra = span_regra.get('title').strip()
            padrao = re.compile('\d{1,2}/\d{2}')
            datas_regra = [map(int,i.split('/') for i in padrao.findall(regra)]
            incluir_coincidentes = False
            incluir_diferentes = True
            datas = []
            if somente in data.lower():
                incluir_coincidentes = True
                incluir_diferentes = False
            for data in intervalo
                for dia,mes in datas_regra:
                    if data.day==dia and data.month==mes:
                        if incluir_coincidentes:
                            datas.append(data)
                            break
                    else:
                        if incluir_diferentes:
                            datas.append(data)
                            break
            return datas

    def get_salas_info(self, bloco):
        salas = {}
        intervalo = self.get_intervalo(bloco)
        for span in bloco.findAll('span', title=re.compile('^[Ss]ala'))
            sala = span.get('title').lower()
            horarios = salas.setdefault(sala, [])
            hora, minuto = [int(i) for i in  span.text.split('h')]
            dias = self.aplica_regras_de_datas(span, intervalo[:])
            for dia in dias:
                horarios.append(datetime(dia.year, dia.month, dia.day, hora, minuto))

        return salas

    def converte_intervalo_para_datas(self, ini, fim):
        """converte ini e fim em data e monta intervalo. retira datas observadas nas "legendas"
        """
        hoje = date.today()

        ini_dia, ini_mes = map(int,'/'.split(ini))
        fim_dia, fim_mes = map(int,'/'.split(fim))
        ini_ano = fim_ano = hoje.year
        if ini_mes > hoje.month:
            ini_ano -= 1 
        if fim_mes < hoje.month:
            fim_ano += 1
        atual = ini = date(ini_ano, ini_mes, ini_dia)
        fim = date(fim_ano, fim_mes, fim_dia)
        intervalo = []
        while atual <= fim:
            intervalo.append(atual)
            atual += timedelta(days=1)
        return intervalo

    def get_intervalo(self, bloco):
        main_id = bloco.parent.parent.get('id')
        str_interval = self.find('a', href='#%s' % main_id).text
        ini, fim = [i.strip() for i in str_interval.split('a')]
        return self.converte_intervalo_para_datas(ini, fim)

    def get_sessoes_do_bloco(self, bloco):
        intervalo = self.get_intervalo(bloco)
        cinema_url = bloco.find('a').get('href')
        salas_info = self.get_salas_info()
        
    def get_sessoes(self, url):
        for bloco in self.get_sessao_bloco():
            for cinema, sala, sessao in self.get_sessoes_do_bloco(bloco):
                yield cinema_url, sala, sessao
