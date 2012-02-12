# coding: utf-8
import urllib2
from cinema import  CinemaParser
from filme import FilmeParser, EmCartazParser

class CinemaCrawler(object):
    url_em_cartaz = "http://www.cinemark.com.br/filmes/em-cartaz"
    urls = ['http://www.cinemark.com.br/programacao/palmas/capim-dourado/31/661',]

    def get_urls(self):
        #TODO: Navegar pelos filmes em cartaz e decobrir as urls de cinema
        cinemas = set()
        em_cartaz = urllib2.urlopen(self.url_em_cartaz)
        urls_filme = EmCartazParser(em_cartaz).urls_filme()
        for url_filme in urls_filme:
            print url_filme
            filme = urllib2.urlopen(url_filme)
            for nome, url in FilmeParser(filme).urls_cinema():
                cinemas.add((nome, url))
        return cinemas

    def get_cinemas(self):
        cinemas = []
        for nome, url in self.get_urls():
            print nome, url
            cinema = urllib2.urlopen(url)
            cinemas.append((nome, CinemaParser(cinema).cinema()))
        return cinemas

if __name__ == "__main__":
    print CinemaCrawler().get_cinemas()

