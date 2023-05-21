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
    