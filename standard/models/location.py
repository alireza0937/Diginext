import json
from django.db import models
from redis_connection import redis_connection
from standard.models.standard import Standard
from user.models import Car
from django.db.models.signals import post_save
from django.dispatch import receiver


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    speed = models.FloatField()
    acceleration = models.FloatField()
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    created_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Locations'
        db_table = 'Locations'

    def __str__(self):
        return self.car_id


@receiver(post_save, sender=Location)
def my_model_post_save(sender, instance: Location, created, **kwargs):
    if created:

        data = {
            'location': instance.pk,
        }
        location_data = json.dumps(data)
        redis_connection.publish_data('diginext', location_data)


