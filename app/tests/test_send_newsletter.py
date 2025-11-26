from datetime import timedelta

import pytest
from django.core.management import call_command
from django.utils import timezone

from .factories import TopicFactory, SubscriberFactory, ContentFactory
from ..management.commands import send_newsletter

pytestmark = pytest.mark.django_db


def run_command():
    call_command("send_newsletter")


def test_happy_path_single_content_two_subscribers(send_mail_spy):
    topic = TopicFactory()
    s1 = SubscriberFactory(topic=topic)
    s2 = SubscriberFactory(topic=topic)
    content = ContentFactory(topic=topic, send_at=timezone.now() - timedelta(minutes=1))

    run_command()

    content.refresh_from_db()

    # Email sent once with both recipients
    assert len(send_mail_spy) == 1
    assert set(send_mail_spy[0]["recipient_list"]) == {s1.email, s2.email}
    assert content.is_sent is True
    assert content.sent_at is not None


def test_content_in_future_not_sent(send_mail_spy):
    topic = TopicFactory()
    SubscriberFactory(topic=topic)
    content = ContentFactory(topic=topic, send_at=timezone.now() + timedelta(hours=1))

    run_command()

    content.refresh_from_db()

    assert len(send_mail_spy) == 0
    assert content.is_sent is False
    assert content.sent_at is None


def test_no_subscribers_marks_content_sent_but_sends_nothing(send_mail_spy):
    topic = TopicFactory()
    content = ContentFactory(topic=topic, send_at=timezone.now() - timedelta(minutes=1))

    run_command()

    content.refresh_from_db()
    assert len(send_mail_spy) == 0
    assert content.is_sent is True
    assert content.sent_at is not None


def test_multiple_contents_processed(send_mail_spy):
    topic1 = TopicFactory(name="Tech")
    topic2 = TopicFactory(name="Sports")

    s1 = SubscriberFactory(topic=topic1)
    s2 = SubscriberFactory(topic=topic2)

    c1 = ContentFactory(topic=topic1, send_at=timezone.now() - timedelta(minutes=5))
    c2 = ContentFactory(topic=topic2, send_at=timezone.now() - timedelta(minutes=2))

    run_command()

    c1.refresh_from_db()
    c2.refresh_from_db()

    # Should have 2 send_mail calls
    assert len(send_mail_spy) == 2

    recipients_sets = [set(call["recipient_list"]) for call in send_mail_spy]
    assert {s1.email} in recipients_sets
    assert {s2.email} in recipients_sets

    assert c1.is_sent is True and c1.sent_at is not None
    assert c2.is_sent is True and c2.sent_at is not None


def test_idempotency_running_twice_does_not_resend(send_mail_spy):
    topic = TopicFactory()
    SubscriberFactory(topic=topic)
    content = ContentFactory(topic=topic, send_at=timezone.now() - timedelta(minutes=1))

    run_command()
    content.refresh_from_db()
    assert content.is_sent is True
    first_sent_count = len(send_mail_spy)

    run_command()
    content.refresh_from_db()

    # still only first run's emails
    assert len(send_mail_spy) == first_sent_count
    assert content.is_sent is True


def test_subscribers_of_other_topics_do_not_receive(send_mail_spy):
    topic1 = TopicFactory()
    topic2 = TopicFactory()

    s1 = SubscriberFactory(topic=topic1)
    SubscriberFactory(topic=topic2)  # should NOT receive

    content = ContentFactory(topic=topic1, send_at=timezone.now() - timedelta(minutes=1))

    run_command()

    assert len(send_mail_spy) == 1
    recipients = send_mail_spy[0]["recipient_list"]
    assert recipients == [s1.email]


def test_send_failure_does_not_mark_content_sent(monkeypatch, send_mail_spy):
    # override spy with failing version just for this test

    def failing_send_mail(*args, **kwargs):
        raise Exception("SMTP failure")

    monkeypatch.setattr(send_newsletter, "send_mail", failing_send_mail)

    topic = TopicFactory()
    SubscriberFactory(topic=topic)
    content = ContentFactory(topic=topic, send_at=timezone.now() - timedelta(minutes=1))

    # This should not raise (command handles exception internally)
    run_command()

    content.refresh_from_db()

    # uur spy from global fixture isn't used here
    # but we can assert the content was not marked as sent
    assert content.is_sent is False
    assert content.sent_at is None


def test_no_pending_content_prints_message(capfd, send_mail_spy):
    run_command()

    # capture stdout
    out, err = capfd.readouterr()
    assert "No pending newsletters found." in out
    assert len(send_mail_spy) == 0
