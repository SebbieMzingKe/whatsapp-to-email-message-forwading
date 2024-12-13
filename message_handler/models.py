from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    whatsapp_number = models.CharField(max_length = 20, unique = True)
    is_online = models.BooleanField(default = True)
    last_seen = models.DateTimeField(auto_now = True)
    # email_forwading_enabled = models.BooleanField(default = True)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    sender_number = models.CharField(max_length = 20)
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now = True)
    is_emailed = models.BooleanField(default = False)
    is_synced = models.BooleanField(default = False)
    forwarded = models.BooleanField(default = True)
    whatsapp_message_id = models.CharField(max_length = 100, unique = True)    