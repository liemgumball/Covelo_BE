from django.urls import path
from .views import *

urlpatterns = [
    path('send/', SendNotification.as_view(), name='send_notification'),
]
