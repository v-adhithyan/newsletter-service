from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.views import health, TopicViewSet, ContentViewSet, SubscriberViewSet

router = DefaultRouter()
router.register(r"topics", TopicViewSet, basename="topic")
router.register(r"subscribers", SubscriberViewSet, basename="subscriber")
router.register(r"contents", ContentViewSet, basename="content")

urlpatterns = [
    path("health/", health),
    path("", include(router.urls)),

]
