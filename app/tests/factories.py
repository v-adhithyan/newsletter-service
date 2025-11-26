import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from app.models import Topic, Subscriber, Content


class TopicFactory(DjangoModelFactory):
    class Meta:
        model = Topic

    name = factory.Sequence(lambda n: f"Topic {n}")


class SubscriberFactory(DjangoModelFactory):
    class Meta:
        model = Subscriber

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    topic = factory.SubFactory(TopicFactory)


class ContentFactory(DjangoModelFactory):
    class Meta:
        model = Content

    topic = factory.SubFactory(TopicFactory)
    text = factory.Faker("sentence")
    send_at = factory.LazyFunction(timezone.now)  # default: send immediately
    is_sent = False
    sent_at = None
