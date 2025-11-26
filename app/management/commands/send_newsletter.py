from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone

from app.models import Content, Subscriber


class Command(BaseCommand):
    help = 'Send newsletter via SMTP at scheduled time'

    def handle(self, *args, **options):
        self.stdout.write("Sending newsletter via SMTP ..")

        now = timezone.now()
        pending_newsletters = Content.objects.filter(is_sent=False, send_at__lte=now).select_related('topic')

        if not pending_newsletters.exists():
            self.stdout.write('No pending newsletters found.')

        for newsletter in pending_newsletters:
            topic = newsletter.topic
            subscribers = Subscriber.objects.filter(topic=topic)
            recipients = [s.email for s in subscribers]

            if not subscribers:
                self.stderr.write(
                    f'No subscribers found for {newsletter.id}. Marked as sent without sending newsletter.')
                newsletter.is_sent = True
                newsletter.sent_at = now
                newsletter.save()

            subject = f"Newsletter - # {topic.name}"
            body = newsletter.text

            try:
                sent_count = send_mail(subject=subject, message=body, from_email=settings.DEFAULT_FROM_EMAIL,
                                       recipient_list=recipients, fail_silently=False, )
                newsletter.is_sent = True
                newsletter.sent_at = timezone.now()
                newsletter.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Sent newsletter successfully, content id: {newsletter.id}, sent email count: {sent_count}'))
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f'Error sending newsletter: {e}, content id: {newsletter.id}')
                )

        self.stdout.write("Done ..")
