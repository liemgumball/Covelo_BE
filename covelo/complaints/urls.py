from django.urls import path
from .views import *

urlpatterns = [
    path('rental_complaint/create', CreateRentalComplaint.as_view(), name='create_rental_complaint'),
    path('bicycle_complaint/create', CreateBicycleComplaint.as_view(), name='create_bicycle_complaint'),
    path('station_complaint/create', CreateStationComplaint.as_view(), name='create_station_complaint'),
]
