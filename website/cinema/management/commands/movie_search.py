from django.core.management.base import BaseCommand, CommandError
from cimena.robos.themoviedb import tmdb

class Command(BaseCommand):
    args = '<movie movie ...>'
    help = 'Search a movie on themoviedb'

    def handle(self, *args, **options):
        for search in args:
            self.stdout.write(search)
            res = tmdb.search(search)
            import ipdb; ipdb.set_trace()