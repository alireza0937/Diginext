from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name_plural = 'Users'
        db_table = 'Users'


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=150, blank=True, null=True)
    number_of_cars = models.IntegerField(blank=True, null=True)
    is_made = models.BooleanField(default=False)

    def __str__(self):
        return str(self.company_name)

    class Meta:
        verbose_name_plural = 'Company'
        db_table = 'Company'
