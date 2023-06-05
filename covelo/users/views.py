from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import *
from .models import CustomUser
import json
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class UserRegistration(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class UserLogin(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(
                request=request, username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                user = CustomUser.objects.get(username=username)
                return Response({'token': token.key, 'id': user.id, 'username': user.username, 'violate_number': user.violate_num})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaveFCMTokenAPIView(generics.GenericAPIView):
    serializer_class = FCMTokenSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        fcm_token = serializer.validated_data['fcm_token']

        try:
            instance = FCMToken.objects.get(user=user)
            instance.fcm_token = fcm_token
            instance.save()
            return Response(serializer.data)
        except FCMToken.DoesNotExist:
            try:
                serializer.save()
            except:
                return Response({'error saving':'fcm_token already exists'})
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetFCMTokenAPIView(generics.RetrieveAPIView):
    serializer_class = FCMTokenSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs['user']
        user = get_object_or_404(CustomUser, id=user_id)
        try:
            fcm_token = user.fcmtoken.fcm_token
            serializer = self.get_serializer(data={'user': user, 'fcm_token': fcm_token})
            serializer.is_valid()
            response_data = serializer.data
            response_data['user'] = user.id  # Serialize user ID instead of the user object
            return Response(response_data)

        except FCMToken.DoesNotExist:
            return Response({'error': 'FCMToken not found'}, status=404)