from django.urls import path
from .views import *

urlpatterns = [
    path('list/<int:user>', listRentalsByUser.as_view(), name='list rental users'),
    path('<int:pk>', detailRental.as_view(), name='detail rental'),
    path('create/', createRental.as_view(), name='create rental'),
    path('end/<int:bicycle>', endRental.as_view(), name='end rental'),
    path('list_by_status/', usingListBicycle.as_view()),
]
