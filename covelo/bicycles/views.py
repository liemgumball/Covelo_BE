from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *
# Create your views here.


class BicycleDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BicycleSerializer

    def get(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        if serializer is not None:
            try:
                bicycle = Bicycle.objects.get(id=pk)
                return Response({'id': bicycle.pk, 'locker_id': bicycle.locker.id, 'station_id': bicycle.get_station().id}, status=status.HTTP_200_OK)
            except:
                return Response({'error': 'This bike is not locked'}, status=status.HTTP_404_NOT_FOUND)
        return Response('error', status=status.HTTP_400_BAD_REQUEST)
