from django.db import models
from rentals.models import Rental
from bicycles.models import Bicycle
from stations.models import Station
from users.models import CustomUser

# Create your models here.


class Complaint(models.Model):
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    is_solved = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title + ' ' + 'solved' if self.is_solved else 'unsolved'


class RentalComplaint(Complaint):
    rental = models.ForeignKey(
        Rental, on_delete=models.DO_NOTHING, related_name='rental_complaint')


class BicycleComplaint(Complaint):
    bicycle = models.ForeignKey(
        Bicycle, on_delete=models.DO_NOTHING, related_name='bicycle_complaint')


class StationComplaint(Complaint):
    station = models.ForeignKey(
        Station, on_delete=models.DO_NOTHING, related_name='station_complaint')
    locker_number = models.SmallIntegerField(null=True)