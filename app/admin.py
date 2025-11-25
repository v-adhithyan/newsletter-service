from django.contrib import admin

from .models import Topic, Subscriber

admin.site.site_header = "Newsletter Service Administration"
admin.site.site_title = "Newsletter Service Admin"
admin.site.index_title = "Welcome to Newsletter Service Administration"

# Register your models here.
admin.site.register(Topic)
admin.site.register(Subscriber)
