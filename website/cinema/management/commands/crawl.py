
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):

    def handle(self, *args, **options):
        print "Starting crawlers"
