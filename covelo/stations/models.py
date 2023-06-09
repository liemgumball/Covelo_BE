from django.db import models
# from bicycles.models import Bicycle
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Station(models.Model):
    location = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveSmallIntegerField(default=1)

    def __str__(self) -> str:
        return self.location


class Locker(models.Model):
    is_locked = models.BooleanField(default=True)
    station = models.ForeignKey(
        Station, on_delete=models.SET_NULL, null=True, related_name='lockers')

    def __str__(self) -> str:
        return self.station.__str__() + " " + str(self.id) + " " + ("locked" if self.is_locked else "unlocked")

    def get_station(self):
        return self.station
