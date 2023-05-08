from django.urls import path
from .views import *

urlpatterns = [
    # path('register/', UserRegistration.as_view(), name='user_register'),
    # path('login/', UserLogin.as_view(), name='user_login'),
    path('station/<int:id>/', station.as_view(), name='station_detail'),
    path('station_list/', stationList.as_view(), name='station_list'),
]
