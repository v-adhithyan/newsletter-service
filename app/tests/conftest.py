import pytest
from django.test import override_settings


@pytest.fixture(autouse=True)
def force_console_backend(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    return settings


@pytest.fixture
def send_mail_spy(monkeypatch):
    sent_emails = []

    def fake_send_mail(subject, message, from_email, recipient_list, fail_silently=False, *args, **kwargs):
        sent_emails.append(
            {
                "subject": subject,
                "message": message,
                "from_email": from_email,
                "recipient_list": list(recipient_list),
            }
        )
        # emulate Django's send_mail returning number of successfully delivered messages
        return len(recipient_list)

    monkeypatch.setattr(
        "app.management.commands.send_newsletter.send_mail", fake_send_mail
    )
    return sent_emails
