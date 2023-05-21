from rest_framework import serializers
from .models import *


class RentalComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalComplaint
        fields = '__all__'


class BicycleComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = BicycleComplaint
        fields = '__all__'


class StationComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationComplaint
        fields = '__all__'
