from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import *
from .serializers import *
# Create your views here.

class createRental(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateRentalSerializer
