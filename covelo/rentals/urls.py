from django.urls import path
from .views import *

urlpatterns = [
    path('create/', createRental.as_view(), name='user_login')
]
