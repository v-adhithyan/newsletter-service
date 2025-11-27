from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Topic, Subscriber, Content
from .serializers import TopicSerializer, SubscriberSerializer, ContentSerializer


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})


class BaseAuthedViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]


class TopicViewSet(BaseAuthedViewSet):
    queryset = Topic.objects.all().order_by("id")
    serializer_class = TopicSerializer


class SubscriberViewSet(BaseAuthedViewSet):
    queryset = Subscriber.objects.select_related("topic").order_by("id")
    serializer_class = SubscriberSerializer


class ContentViewSet(BaseAuthedViewSet):
    queryset = Content.objects.select_related("topic").order_by("send_at")
    serializer_class = ContentSerializer
