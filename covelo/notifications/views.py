from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *

# Create your views here.

class SendNotification(generics.GenericAPIView):
    serializer_class = NotificationSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = NotificationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         instance = serializer.save()
    #         instance.send_notification_view()
    #         return Response(instance.title,status=status.HTTP_200_OK)
    #     return Response('error', status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        noti = Notification.objects.all().first()
        return noti.send_notification_view()