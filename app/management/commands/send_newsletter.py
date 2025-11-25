from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Send newsletter via SMTP at scheduled time'

    def handle(self, *args, **options):
        print("Sending newsletter via SMTP ..")
        print("Done ..")
