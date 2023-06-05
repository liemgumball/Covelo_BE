from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *

# Create your views here.


class CreateRentalComplaint(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RentalComplaintSerializer


class CreateBicycleComplaint(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BicycleComplaintSerializer


class CreateStationComplaint(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = StationComplaintSerializer


class ListStationComplaints(generics.ListAPIView):
    # queryset = StationComplaint.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = StationComplaintSerializer
    def get_queryset(self):
        user_id = self.kwargs.get('user')
        queryset = StationComplaint.objects.filter(user=user_id)
        return queryset


class ListRentalComplaints(generics.ListAPIView):
    # queryset = RentalComplaint.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RentalComplaintSerializer
    def get_queryset(self):
        user_id = self.kwargs.get('user')
        queryset = RentalComplaint.objects.filter(user=user_id)
        return queryset


class ListBicycleComplaints(generics.ListAPIView):
    # queryset = BicycleComplaint.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = BicycleComplaintSerializer
    def get_queryset(self):
        user_id = self.kwargs.get('user')
        queryset = BicycleComplaint.objects.filter(user=user_id)
        return queryset
