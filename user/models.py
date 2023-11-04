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


class Car(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.company_id)

    class Meta:
        verbose_name_plural = 'Cars'
        db_table = 'Cars'
