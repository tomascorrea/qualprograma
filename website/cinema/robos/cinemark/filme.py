# coding: utf-8
import BeautifulSoup

BASE_URL = "http://www.cinemark.com.br"


class EmCartazParser(BeautifulSoup.BeautifulSoup):
    def urls_filme(self):
        urls = []
        for attrs in [i.find("a").attrs for i in self.findAll("div", {"class":"texto_item"})]:
            for attr, value in attrs:
                if attr == u'href':
                    urls.append(BASE_URL+value)
        return urls
            

class FilmeParser(BeautifulSoup.BeautifulSoup):
    def urls_cinema(self):
        urls = []
        for tag_a in [i.find("a") for i in self.findAll("div", {"class":"filme"})]:
            nome = tag_a.string
            for attr, value in tag_a.attrs:
                if attr == u"href":
                    urls.append((nome, BASE_URL+value))
        return urls

