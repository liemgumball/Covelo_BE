from django.urls import path
from .views import *

urlpatterns = [
    # path('register/', UserRegistration.as_view(), name='user_register'),
    # path('login/', UserLogin.as_view(), name='user_login'),
    path('<int:pk>/', BicycleDetail.as_view(), name='bicycle_detail'),
]
