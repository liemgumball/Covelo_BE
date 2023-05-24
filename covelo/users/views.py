from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import *
from .models import CustomUser
from django.http.response import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
import json


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


@api_view(['POST'])
def save_user_token(request):
    """
    Example {
    "user_id" : "1",
    "fcm_token" : "aldkjaldkaj"
    }


    """
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        token = request.data.get('fcm_token')
        # Lưu thông tin vào session
        request.session['user_{user_id}'] = {
            'user_id': user_id, 'fcm_token': token}
        response = request.session['user_{user_id}']
        response = json.dumps(response)
        return Response(json.loads(response), status=status.HTTP_201_CREATED)
    return Response('errors', status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_user_token(request, user_id):
    if request.method == 'GET':
        response = request.session['user_{user_id}']
        response = json.dumps(response)
        return Response(json.loads(response), status=status.HTTP_200_OK)
    return Response('errors', status=status.HTTP_400_BAD_REQUEST)
