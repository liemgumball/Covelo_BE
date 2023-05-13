from rest_framework import serializers
from .models import *

class BicycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = ['id']