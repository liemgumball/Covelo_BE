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
    serializer_class = StationDetailSerializer
    def get_queryset(self):
        return Station.objects.all()

class updateLocker(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LockerSerializer
    queryset = Locker.objects.all()