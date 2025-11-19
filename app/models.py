from django.db import models

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Content(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    text = models.TextField(blank=False, null=False)
    send_at = models.DateTimeField(auto_now_add=False, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.topic} - {self.text}'

class User(models.Model):
    email = models.EmailField(unique=True, blank=False, null=False)
    topic = models.OneToOneField(Topic, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
