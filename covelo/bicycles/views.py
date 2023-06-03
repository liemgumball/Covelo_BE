from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.permissions import AllowAny 
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.filters import SearchFilter
# Create your views here.


class BicycleDetail(generics.RetrieveAPIView):
    queryset = Bicycle.objects.all()
    permission_classes = [AllowAny]
    serializer_class = BicycleSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance is not None:
            try:
                return Response({'id': instance.id,
                                 'magnetic_key': instance.magnetic_key,
                                 'locker_id': instance.locker.id,
                                 'station_id': instance.get_station().id},
                                status=status.HTTP_200_OK)
            except:
                return Response({'error': 'This bike is not locked'}, status=status.HTTP_404_NOT_FOUND)
        return Response('error', status=status.HTTP_400_BAD_REQUEST)


class BicycleDetailByMagneticKey(generics.RetrieveAPIView):
    queryset = Bicycle.objects.all()
    permission_classes = [AllowAny]
    serializer_class = BicycleSerializer
    lookup_field = 'magnetic_key'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance is not None:
            try:
                return Response({'id': instance.id,
                                 'magnetic_key': instance.magnetic_key,
                                 'locker_id': instance.locker.id,
                                 'station_id': instance.get_station().id},
                                status=status.HTTP_200_OK)
            except:
                return Response({'error': 'This bike is not locked'}, status=status.HTTP_404_NOT_FOUND)
        return Response('error', status=status.HTTP_400_BAD_REQUEST)


class BicycleUpdate(generics.UpdateAPIView):
    queryset = Bicycle.objects.all()
    permission_classes = [AllowAny]
    serializer_class = BicycleUpdateSerializer
    lookup_field = 'magnetic_key'

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            locker = instance.get_locker()
            if locker is not None:
                locker.is_locked = True
                locker.save()
                return Response({
                    'id': instance.id,
                    'locker_id': instance.locker.id,
                    'station_id': instance.get_station().id, },
                    status=status.HTTP_200_OK)
            else:
                return Response({
                    'id': instance.id,
                    'locker_id': 'null', },
                    status=status.HTTP_200_OK)
        else:
            return Response({"message": "Failed", "details": serializer.errors})
        
class UsingBicycleList(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BicycleSerializer
    lookup_field = 'locker'
    queryset = Bicycle.objects.filter(locker__isnull=True)
