from django.db import models
from user.models import User, Company


class Standard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    minimum_velocity = models.IntegerField(blank=True, null=True)
    maximum_velocity = models.IntegerField(blank=True, null=True)
    minimum_acceleration = models.IntegerField(blank=True, null=True)
    maximum_acceleration = models.IntegerField(blank=True, null=True)
    in_tehran = models.BooleanField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Standards'
        db_table = 'Standards'

    def __str__(self):
        return self.in_tehran
