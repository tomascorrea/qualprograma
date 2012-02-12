# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.management.base import NoArgsCommand
from cinema.robos.cinemark.crawler import CinemaCrawler
from cinema.robos.themoviedb import tmdb
from cinema.models import Filme

class Command(NoArgsCommand):

    def handle(self, *args, **options):
        print "Starting crawlers"
        import ipdb; ipdb.set_trace()
        Filme.objects.all().delete()
        for titulo in CinemaCrawler().get_titulos():
            print titulo
            try:
                results = tmdb.search(titulo)
                if results:
                    for res in results:
                        info = res.info()
                        #import pdb; pdb.set_trace()
                        filme, created = Filme.objects.get_or_create(titulo=titulo)
                        if created:
                            filme.sinopse = res['overview']
                            filme.url = res['url']
                            filme.categorias = ", ".join(info['categories']['genre'].keys())
                            filme.lancamento = datetime.strptime(info['released'], "%Y-%m-%d")
                            filme.save()
                        print res
            except Exception, e:
                print e


        

