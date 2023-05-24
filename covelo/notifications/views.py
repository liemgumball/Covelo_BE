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

    def send_notification_view(self):
        expo_push_token = "ExponentPushToken[QPiataO0qw6ZYNeVSxoHT2]"
        # self.send_notification(
        #     "New message", "You have a new message", {}, expo_push_token)
        self.send_push_notification(expo_push_token)
        # return Response("Notification sent")

    def send_push_notification(self, expo_push_token):
        message = {
            'to': expo_push_token,
            'sound': 'default',
            'title': 'Original Title',
            'body': 'And here is the body!',
            'data': {'someData': 'goes here'}
        }

        headers = {
            'Accept': 'application/json',
            'Accept-encoding': 'gzip, deflate',
            'Content-Type': 'application/json'
        }

        response = requests.post(
            'https://exp.host/--/api/v2/push/send', headers=headers, json=message)
        response.raise_for_status()  # Raises an exception if the request was not successful
        return Response(response.json())

    def get(self, request, *args, **kwargs):
        return self.send_notification_view()
    