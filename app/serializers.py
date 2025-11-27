from rest_framework import serializers

from .models import Topic, Subscriber, Content


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class SubscriberSerializer(serializers.ModelSerializer):
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())

    class Meta:
        model = Subscriber
        fields = '__all__'
        read_only_fields = ["created_at", "updated_at"]


class ContentSerializer(serializers.ModelSerializer):
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())

    class Meta:
        model = Content
        fields = '__all__'
        read_only_fields = ["is_sent", "sent_at", "created_at", "updated_at"]
