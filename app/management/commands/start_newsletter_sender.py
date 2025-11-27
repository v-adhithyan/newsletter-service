import time

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = 'Send newsletter via SMTP at scheduled time'

    def handle(self, *args, **options):
        while True:
            call_command('send_newsletter')
            time.sleep(60)
