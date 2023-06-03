from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import *
from .serializers import *
import requests
import json
from rest_framework.filters import SearchFilter
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

    def send_push_notification(self, request, rental):
        user_id =  rental.user.id
        try:
            expo_push_token = request.session['user_{user_id}']
            expo_push_token = json.dumps(expo_push_token)
            expo_push_token = json.loads(expo_push_token)
            message = {
                'to': expo_push_token,
                'sound': 'default',
                'title': 'Test Push Notification',
                'body': 'And here is the body!',
                'data': {'id': rental.id,
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
            return Response(response.json())
        except:
            return Response("Failed to send: no fcm_token in session")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rental = serializer.save()
        headers = self.get_success_headers(serializer.data)
        self.send_push_notification(request, rental)
        return Response({'id': rental.id,
                         'user': rental.user.id,
                         'bicycle': rental.bicycle.id,
                         'status': rental.status,
                         'time_begin': rental.time_begin,
                         'start_station': rental.start_station.id},
                        status=status.HTTP_201_CREATED, headers=headers)


class endRental(generics.UpdateAPIView):
    queryset = Rental.objects.all()
    permission_classes = [AllowAny]
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
    
class usingListBicycle(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = UsingBicycleListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['status']

    def get_queryset(self):
        status = self.request.query_params.get('status')
        queryset = Rental.objects.all()
        if status:
            queryset = queryset.filter(status=status)
        return queryset
