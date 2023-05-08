from django.db import models
from users.models import CustomUser
from bicycles.models import Bicycle
from stations.models import Station

# Create your models here.


class Rental(models.Model):
    options = (
        ('wait_for_comfirm', 'Wait for comfirm'),
        ('canceled', 'Canceled'),
        ('using', 'Using'),
        ('finished', 'Finished'),
        ('overtime', 'Overtime'),
    )

    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, related_name='user_rental', default='')
    bicycle = models.ForeignKey(
        Bicycle, on_delete=models.DO_NOTHING, related_name='bicycle_rental', default='')
    status = models.CharField(
        max_length=50, choices=options, default='wait_for_comfirm')
    time_begin = models.DateTimeField(auto_now_add=True)
    time_end = models.DateTimeField(default='', blank=True, null=True)
    start_station = models.ForeignKey(
        Station, on_delete=models.DO_NOTHING, related_name='start_station_rental')
    end_station = models.ForeignKey(
        Station, on_delete=models.DO_NOTHING, related_name='end_station_rental')
    is_violated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.__str__() + ' ' + str(self.id)