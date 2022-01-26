from django.db import models
from .phone_validator import validate_phone


# Create your models here.
class City(models.Model):
    city = models.CharField(max_length=20)


class Delivery(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=13, validators=[validate_phone])

    delivery_city = models.ForeignKey(City, on_delete=models.SET_NULL)
    self_delivery = models.BooleanField(default=False)
    courier = models.BooleanField(default=False)
    address = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Delivery ID = {self.pk} for {self.first_name} {self.last_name}, city: {self.delivery_city}'

    @property
    def delivery_info(self):
        return f'ID:{self.pk}, {self.first_name} {self.last_name}, {self.delivery_city},' \
               f'{self.address}, phone: {self.phone} ...'
