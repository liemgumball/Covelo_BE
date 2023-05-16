from rest_framework import serializers
from .models import *

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'

class CreateRentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['user', 'bicycle', 'start_station']
        # fields = '__all__'

class UpdateRentalSerializer(serializers.ModelSerializer):
    time_end = serializers.DateTimeField(default=timezone.now)
    end_station_id = serializers.IntegerField(required=True)
    status = serializers.CharField(default='finished')
    # is_violated = serializers.BooleanField(default=False)
    class Meta:
        model = Rental
        fields = ['end_station_id', 'time_end', 'status']

