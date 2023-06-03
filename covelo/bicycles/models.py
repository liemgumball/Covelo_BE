from django.db import models
from django.utils import timezone
from stations.models import Locker

# Create your models here.


class BicycleStock(models.Model):
    brand = models.CharField(max_length=50, unique=True)
    model = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(default=timezone.now)
    price_per_unit = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self) -> str:
        return self.brand + ' ' + self.model + ' ' + str(self.date_created.date())


class Bicycle(models.Model):
    options = (
        ('good', 'Good'),
        ('damaged', 'Damaged'),
        ('liquidated', 'Liquidated'),
    )
    magnetic_key = models.CharField(max_length=100, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=options, default='good')
    bicycle_stock = models.ForeignKey(
        BicycleStock, on_delete=models.SET_NULL, null=True)
    locker = models.OneToOneField(
        Locker, on_delete=models.SET_NULL, null=True, related_name='bike', blank=True)

    def __str__(self) -> str:
        return str(self.id) + " " + self.status + " locker:" + str(self.locker)

    def get_station(self):
        return self.locker.get_station()

    def set_locker_null(self):
        self.locker = None
        return self.locker

    def get_locker(self):
        return self.locker
