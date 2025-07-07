from django.core.management.base import BaseCommand 
from monitor.services.metrics_server import serve 

class Command(BaseCommand):
    help = 'Starts the gPRC metrics server'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting gRPC metrics server...'))
        serve()