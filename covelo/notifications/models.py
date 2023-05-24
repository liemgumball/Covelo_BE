from django.db import models
from rest_framework.response import Response
from exponent_server_sdk import PushMessage, PushClient
import requests
import json

# Create your models here.


class Notification(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=500, blank=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title + ' ' + str(self.is_sent)
