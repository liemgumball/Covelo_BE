from rest_framework import serializers
from .models import *

class LockerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locker
        fields = ['id','is_locked','bike']

class BikeLockerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locker
        feilds = ['bike']
    
class StationDetailSerializer(serializers.ModelSerializer):
    lockers = LockerSerializer(many=True)
    class Meta:
        model = Station
        fields = ['id', 'location','lockers']

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['id', 'location']