from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *

# Create your views here.
class stationList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Station.objects.all()
    serializer_class = StationSerializer

class station(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = StationSerializer
    queryset = Station.objects.all()