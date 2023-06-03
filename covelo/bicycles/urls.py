from django.urls import path
from .views import *

urlpatterns = [
    path('id=<int:pk>/', BicycleDetail.as_view(), name='bicycle_detail'),
    path('magnetic_key=<str:magnetic_key>/', BicycleDetailByMagneticKey.as_view(), name='bicycle_detail_by_magnetic_key'),
    path('update/<str:magnetic_key>', BicycleUpdate.as_view(), name='bicycle_update'),
    # path('list/', UsingBicycleList.as_view()),
]
