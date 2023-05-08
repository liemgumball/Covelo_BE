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

class station(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, id):
        try:
            station = Station.objects.get(id=id)
            serializer = StationDetailSerializer(station)
            return Response(serializer.data)
        except Station.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)