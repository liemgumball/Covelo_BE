from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *
import requests, json
# Create your views here.


class listRentalsByUser(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RentalListSerializer
    lookup_field = 'user'

    def get_queryset(self):
        user_id = self.kwargs['user']
        return Rental.objects.filter(user=user_id)


class detailRental(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RentalDetailSerializer
    queryset = Rental.objects.all()


class createRental(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateRentalSerializer

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rental = serializer.save()
        headers = self.get_success_headers(serializer.data)
        self.send_notification_view()
        return Response({'id': rental.id,
                         'user': rental.user.id,
                         'bicycle': rental.bicycle.id,
                         'status': rental.status,
                         'time_begin': rental.time_begin,
                         'start_station': rental.start_station.id},
                        status=status.HTTP_201_CREATED, headers=headers)


class endRental(generics.UpdateAPIView):
    queryset = Rental.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UpdateRentalSerializer
    lookup_field = 'bicycle'

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({'id': instance.id,
                             'user_id': instance.user.id,
                             'bicycle': instance.bicycle.id,
                             'status': instance.status,
                             'start_station': instance.start_station.id,
                             'end_station': instance.end_station.id,
                             'time_begin': instance.time_begin,
                             'time_end': instance.time_end,
                             'is_violated': instance.is_violated,
                             'status': instance.status, },
                            status=status.HTTP_200_OK)
        return Response('error', status=status.HTTP_400_BAD_REQUEST)
