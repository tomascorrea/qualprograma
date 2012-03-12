# -*- coding: utf-8 -*-
import logging
from django.core.management.base import NoArgsCommand
from cinema.robos.cinemark.crawler import SessaoCrawler
from cinema.models import Sessao, Cinema

logger = logging.getLogger('qualprograma.robos')

class Command(NoArgsCommand):
    
    def handle(self, *args, **options):
        Sessao.objects.all().delete()
        for sessao in SessaoCrawler().get_sessoes():
            print sessao
