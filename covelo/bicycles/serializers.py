from rest_framework import serializers
from .models import *

class BicycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = '__all__'

class BicycleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = ['locker']