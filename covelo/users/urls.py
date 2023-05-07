from django.urls import path
from .views import *

urlpatterns = [
    # path('register/', UserRegistration.as_view(), name='user_register'),
    # path('login/', UserLogin.as_view(), name='user_login'),
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login')
]