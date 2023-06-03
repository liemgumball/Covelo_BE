from django.urls import path
from .views import *
import requests

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('fcm_token/save', UserTokenSaveAPIView.as_view(), name='save_token'),
    path('fcm_token/<int:user_id>', UserTokenAPIView.as_view(), name='get_token'),
]
