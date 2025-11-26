from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from app.models import Content, Subscriber


class ContentAdminForm(ModelForm):
    class Meta:
        model = Content
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        data = kwargs.get('data', None)
        topic = None
        if data and 'topic' in data:
            topic_id = int(data.get('topic', 0))
            from app.models import Topic
            topic = get_object_or_404(Topic, id=topic_id)
        else:
            if self.instance and self.instance.pk:
                topic = self.instance.topic
            else:
                topic_id = self.initial.get('topic') if hasattr(self, 'initial') else None
                if topic_id:
                    from app.models import Topic
                    topic = get_object_or_404(Topic, id=topic_id)

        if topic:
            self.fields['recipients'].queryset = Subscriber.objects.filter(topic=topic)
        else:
            self.fields['recipients'].queryset = Subscriber.objects.none()

    def clean(self):
        cleaned = super().clean()
        topic = cleaned.get('topic')
        recipients = cleaned.get('recipients')
        if recipients and topic:
            invalid = [r.email for r in recipients if r.topic_id != topic.id]
            if invalid:
                raise ValidationError(
                    "Selected recipients do not all belong to the chosen topic: %s" % ", ".join(invalid))
        return cleaned
