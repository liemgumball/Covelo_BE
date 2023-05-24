from django.urls import path
from .views import *
import requests

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('fcm_token/save', save_user_token, name='save_token'),
    path('fcm_token/<int:user_id>', get_user_token, name='get_token'),
]
