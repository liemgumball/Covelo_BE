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