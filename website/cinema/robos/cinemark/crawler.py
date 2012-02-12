# coding: utf-8
import logging
import urllib2
from cinema_parser import  CinemaParser
from filme_parser import FilmeParser, EmCartazParser
from cinema.models import Rede

logger = logging.getLogger('qualprograma.robos')

class CinemaCrawler(object):
    url_em_cartaz = "http://www.cinemark.com.br/filmes/em-cartaz"
    urls = ['http://www.cinemark.com.br/programacao/palmas/capim-dourado/31/661',]

    def get_urls(self):
        #TODO: Navegar pelos filmes em cartaz e decobrir as urls de cinema
        cinemas = set()
        em_cartaz = urllib2.urlopen(self.url_em_cartaz)
        urls_filme = EmCartazParser(em_cartaz).urls_filme()
        for url_filme in urls_filme:
            filme = urllib2.urlopen(url_filme)
            for nome, url in FilmeParser(filme).urls_cinema():
                cinemas.add((nome, url))
        return cinemas

    def get_cinemas(self):
        cinemas = []
        rede, _ = Rede.objects.get_or_create(nome=u"Cinemark", url=u"www.cinemark.com.br")
        for nome, url in self.get_urls():
            logger.info(':'.join([nome, url]))
            cinema = urllib2.urlopen(url)
            cinemas.append((nome, rede, CinemaParser(cinema).cinema()))
        return cinemas

    def get_titulos(self):
        em_cartaz = urllib2.urlopen(self.url_em_cartaz)
        return EmCartazParser(em_cartaz).get_titulos()



if __name__ == "__main__":
    print CinemaCrawler().get_cinemas()
