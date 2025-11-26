from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import Topic, Subscriber, Content

admin.site.site_header = "Newsletter Service Administration"
admin.site.site_title = "Newsletter Service Admin"
admin.site.index_title = "Welcome to Newsletter Service Administration"

# Register your models here.
admin.site.register(Subscriber)

# these models are by default displayed in admin, we don't need this
# so manually removing them from admin
admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'send_newsletter_email')
    search_fields = ('name',)

    def send_newsletter_email(self, topic):
        app_label = Content._meta.app_label
        model_name = Content._meta.model_name
        add_url = reverse('admin:%s_%s_add' % (app_label, model_name))
        params = {'topic': str(topic.id)}
        url = f'{add_url}?{urlencode(params)}'
        return format_html('<a class="button" href="{}">Send email</a>', url)

    send_newsletter_email.short_description = "Send newsletter email"
    send_newsletter_email.allow_tags = True


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'text', 'send_at', 'is_sent')
    list_filter = ('topic', 'is_sent')
    search_fields = ('topic', 'text')
    # hide certain fields in form
    exclude = ('is_sent', 'sent_at',)

    # when send newsletter email action is clicked in topic admin,
    # we redirect to this with params containing topic id,
    # use it to display subscriber emails
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request) or {}
        topic = request.GET.get('topic')
        if topic:
            initial['topic'] = topic
        return initial
