from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import *
from .serializers import *
import requests
import json
from rest_framework.filters import SearchFilter
import threading
# Create your views here.


class listRentalsByUser(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = RentalListSerializer
    lookup_field = 'user'

    def get_queryset(self):
        user_id = self.kwargs['user']
        return Rental.objects.filter(user=user_id)


class detailRental(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = RentalDetailSerializer
    queryset = Rental.objects.all()


class createRental(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateRentalSerializer

    def send_create_notification(self, rental, expo_push_token):
        try:
            message = {
                'to': expo_push_token,
                'sound': 'default',
                'title': 'Bắt đầu thuê xe!',
                'body': 'Nhấn để xem thông tin',
                'data': {
                    'id': rental.id,
                    'user': rental.user.id,
                    'bicycle': rental.bicycle.id,
                    'start_station': rental.start_station.id,
                    'time_begin': rental.time_begin.isoformat(),
                    'status': rental.status,
                }
            }

            headers = {
                'Accept': 'application/json',
                'Accept-encoding': 'gzip, deflate',
                'Content-Type': 'application/json'
            }

            response = requests.post(
                'https://exp.host/--/api/v2/push/send', headers=headers, json=message)
            response.raise_for_status()  # Raises an exception if the request was not successful
            return response.json()
        except:
            return "Failed to send: no fcm_token in session"

    def send_violate_notification(self, rental, expo_push_token):
        try:
            message = {
                'to': expo_push_token,
                'sound': 'default',
                'title': 'Bạn đã hết thời gian cho mượn!',
                'body': 'Nhấn để xem thông tin',
                'data': {
                    'id': rental.id,
                    'user': rental.user.id,
                    'bicycle': rental.bicycle.id,
                    'start_station': rental.start_station.id,
                    'time_begin': rental.time_begin.isoformat(),
                    'status': rental.status,
                    'is_violated': rental.is_violated,
                }
            }

            headers = {
                'Accept': 'application/json',
                'Accept-encoding': 'gzip, deflate',
                'Content-Type': 'application/json'
            }

            response = requests.post(
                'https://exp.host/--/api/v2/push/send', headers=headers, json=message)
            response.raise_for_status()  # Raises an exception if the request was not successful
            return response.json()
        except:
            return "Failed to send: no fcm_token in session"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        bicycle = serializer.validated_data['bicycle']
        if bicycle.locker:
            try:
                expo_push_token = user.fcmtoken.fcm_token
                locker = bicycle.get_locker()
                locker.is_locked = False
                locker.save()
                bicycle.set_locker_null()
                bicycle.save()
                instance = serializer.save()
                self.send_create_notification(
                    instance, expo_push_token)

                def check_rental_violation():
                    # Retrieve the rental from the database
                    rental = Rental.objects.get(pk=instance.pk)
                    if rental.status == 'using' and not rental.is_violated:
                        # Set is_violated to True
                        user = rental.user
                        user.violate_num = user.violate_num + 1
                        user.save()
                        rental.is_violated = True
                        rental.status = 'overtime'
                        rental.save()
                        # Trigger a notification to the user
                        self.send_violate_notification(
                            rental, expo_push_token)

                # Start a background task to check for violation after 5 minutes
                timer = threading.Timer(300, check_rental_violation)
                timer.start()

            except:
                return Response({'error': 'FCM token is missing or empty.'}, status=400)
        else:
            return Response({'error': 'Bicycle is not available or is not locked'}, status=400)

        headers = self.get_success_headers(serializer.data)
        return Response({
            'id': instance.id,
            'user': instance.user.id,
            'bicycle': instance.bicycle.id,
            'status': instance.status,
            'time_begin': instance.time_begin,
            'start_station': instance.start_station.id
        }, status=status.HTTP_201_CREATED, headers=headers)


class endRental(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UpdateRentalSerializer

    def get_object(self):
        attribute_value = self.kwargs.get('bicycle')
        instance = Rental.objects.filter(
            Q(bicycle=attribute_value) & (
                Q(status="using") | Q(status="overtime"))
        )
        if instance.exists():
            return instance.first()
        else:
            # return Response({'error': 'Rental not found.'}, status=404)
            return None

    def send_end_notification(self, rental, expo_push_token):
        try:
            message = {
                'to': expo_push_token,
                'sound': 'default',
                'title': 'Kết thúc chuyến xe!',
                'body': 'Nhấn để xem thông tin',
                'data': {'id': rental.id,
                         'user': rental.user.id,
                         'bicycle': rental.bicycle.id,
                         'start_station': rental.start_station.id,
                         'end_station': rental.end_station.id,
                         'time_begin': rental.time_begin.isoformat(),
                         'time_end': rental.time_end.isoformat(),
                         'status': rental.status,
                         'is_violated': rental.is_violated,
                         }
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
        except:
            return Response("Failed to send: no fcm_token in session")

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is not None:
            updated_data = {'end_station_id': request.data.get('end_station_id'),
                            'time_end': timezone.now(),
                            'status': 'finished'}
            serializer = self.get_serializer(
                instance, data=updated_data, partial=True)
        else:
            return Response({'error': 'Rental not found.'}, status=404)
        if serializer.is_valid():
            instance = serializer.save()
            try:
                expo_push_token = instance.user.fcmtoken.fcm_token
            # if expo_push_token is not None:
                self.send_end_notification(instance, expo_push_token)
            except:
                return Response({'error': 'Updated but FCM token is missing or empty.'}, status=400)
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


class usingListBicycle(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = RentalListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['status']

    def get_queryset(self):
        status = self.request.query_params.get('status')
        queryset = Rental.objects.all()
        if status:
            queryset = queryset.filter(status=status)
        return queryset
