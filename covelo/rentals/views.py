from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *
# Create your views here.


class createRental(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateRentalSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rental = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response({'id': rental.id,
                         'user': rental.user.id,
                         'bicycle': rental.bicycle.id,
                         'status': rental.status,
                         'time_begin': rental.time_begin,
                         'start_station': rental.start_station.id},
                        status=status.HTTP_201_CREATED)
