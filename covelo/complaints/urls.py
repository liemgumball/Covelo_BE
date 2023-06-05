from django.urls import path
from .views import *

urlpatterns = [
    path('rental_complaint/create', CreateRentalComplaint.as_view(), name='create_rental_complaint'),
    path('bicycle_complaint/create', CreateBicycleComplaint.as_view(), name='create_bicycle_complaint'),
    path('station_complaint/create', CreateStationComplaint.as_view(), name='create_station_complaint'),
    path('station_complaint/list/<int:user>', ListStationComplaints.as_view(), name='list_station_complaint'),
    path('rental_complaint/list/<int:user>', ListRentalComplaints.as_view(), name='list_rental_complaint'),
    path('bicycle_complaint/list/<int:user>', ListBicycleComplaints.as_view(), name='list_bicycle_complaint'),
]
