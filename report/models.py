from django.db import models


class CarLocation(models.Model):
    car = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    st_id = models.IntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.car)

    class Meta:
        verbose_name_plural = 'CarLocations'
        db_table = 'CarLocations'

