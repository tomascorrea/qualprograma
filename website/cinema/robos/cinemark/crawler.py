# coding: utf-8
import logging
import requests
from cinema_parser import  CinemaParser
from sessao_parser import SessaoParser
from filme_parser import FilmeParser, EmCartazParser
from cinema.models import Rede

logger = logging.getLogger('qualprograma.robos')
CINEMARK_URL = 'http://www.cinemark.com.br'

class Crawler(object):
    url_em_cartaz = "http://www.cinemark.com.br/filmes/em-cartaz"

    def get_urls_filmes(self):
        em_cartaz = requests.get(self.url_em_cartaz)
        return EmCartazParser(em_cartaz.text).urls_filme()


class CinemaCrawler(Crawler):

    def get_urls(self):
        #TODO: Navegar pelos filmes em cartaz e decobrir as urls de cinema
        cinemas = set()
        for url_filme in self.get_urls_filmes():
            filme = requests.get(url_filme)
            for nome, url in FilmeParser(filme.text).urls_cinema():
                cinemas.add((nome, url))
        return cinemas

    def get_cinemas(self):
        cinemas = []
        rede, _ = Rede.objects.get_or_create(nome=u"Cinemark", url=u"www.cinemark.com.br")
        for nome, url in self.get_urls():
            logger.info(':'.join([nome, url]))
            cinema = requests.get(url)
            cinemas.append((nome, url, rede, CinemaParser(cinema.text).cinema()))
        return cinemas

    def get_titulos(self):
        em_cartaz = requests.get(self.url_em_cartaz)
        return EmCartazParser(em_cartaz.text).get_titulos()

class SessaoCrawler(Crawler):

    def get_sessoes(self):
        sessoes = []
        for url_filme in self.get_urls_filmes():
            filme = requests.get(url_filme)
            for sala, sessao in SessaoParser(filme.text).get_sessoes(url=url_filme):
                sessoes.extend(sala, sessao)
        return sessoes


if __name__ == "__main__":
    print CinemaCrawler().get_cinemas()
