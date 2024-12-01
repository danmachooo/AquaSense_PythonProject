from django.core.management.base import BaseCommand
from monitoring.arduino_interface import read_arduino_data

class Command(BaseCommand):
    help = 'Starts collecting data from Arduino'

    def handle(self, *args, **options):
        self.stdout.write('Starting Arduino data collection...')
        read_arduino_data()