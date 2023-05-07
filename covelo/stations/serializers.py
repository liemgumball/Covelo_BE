from rest_framework import serializers
from .models import *

class LockerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locker
        fields = ['id','is_locked']
    
class StationSerializer(serializers.ModelSerializer):
    lockers = LockerSerializer(many=True)
    class Meta:
        model = Station
        fields = ['id', 'location','lockers']