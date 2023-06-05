from django.db import models
from django.utils import timezone
from users.models import CustomUser
from bicycles.models import Bicycle
from stations.models import Station

# Create your models here.


class Rental(models.Model):
    options = (
        ('canceled', 'Canceled'),
        ('using', 'Using'),
        ('finished', 'Finished'),
        ('overtime', 'Overtime'),
    )

    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='user_rental')
    bicycle = models.ForeignKey(
        Bicycle, on_delete=models.DO_NOTHING, related_name='bicycle_rental')
    status = models.CharField(
        max_length=50, choices=options, default='using')
    time_begin = models.DateTimeField(default=timezone.now)
    time_end = models.DateTimeField(blank=True, null=True)
    start_station = models.ForeignKey(
        Station, on_delete=models.DO_NOTHING, related_name='start_station_rental')
    end_station = models.ForeignKey(
        Station, on_delete=models.DO_NOTHING, related_name='end_station_rental', null=True)
    is_violated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.id) + ' ' + self.user.__str__() + "--------------Status:" + str(self.status) + "----------Bicycle:" + str(self.bicycle.id)
