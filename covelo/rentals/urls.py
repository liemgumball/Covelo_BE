from django.urls import path
from .views import *

urlpatterns = [
    path('create/', createRental.as_view(), name='create rental'),
    # path('end/<str:magnetic_key>', endRental.as_view(), name='end rental'),
    path('end/<int:bicycle>', endRental.as_view(), name='end rental'),
]
