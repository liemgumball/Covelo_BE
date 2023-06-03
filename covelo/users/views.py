from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import *
from .models import CustomUser
from rest_framework.decorators import api_view
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


class UserTokenAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id):
        response = request.session.get(f'user_{user_id}_token')
        response = json.dumps(response)
        response = json.loads(response)
        return Response({"fcm_token": response}, status=status.HTTP_200_OK)


class UserTokenSaveAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='User ID'
                ),
                'fcm_token': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Token used to push notification'
                )
            }
        )
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        token = request.data.get('fcm_token')
        # Lưu thông tin vào session
        try:
            user = CustomUser.objects.get(id=user_id)
            request.session[f'user_{user.id}_token'] = token
            request.session.modified = True
            response = request.session.get(f'user_{user.id}_token')
            response = json.dumps(response)
            response = json.loads(response)
            return Response({"Status": "successed", "fcm_token": response}, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'User not existed'}, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='User ID'
                ),
            }
        )
    )
    def delete(self, request):
        user_id = request.data.get('user_id')
        if f'user_{user_id}_token'in request.session:
            del request.session[f'user_{user_id}_token']
            request.session.modified = True
            return Response({'message': 'FCM token deleted from session'})
        else:
            return Response({'error': 'FCM token not found in session'})
