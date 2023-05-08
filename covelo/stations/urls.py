from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/', station.as_view(), name='station_detail'),
    path('list/', stationList.as_view(), name='station_list'),
]
