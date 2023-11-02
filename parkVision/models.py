from django.db import models

# Create your models here.
class Car(models.Model):
    car_number = models.CharField(max_length=30)
    slot_number = models.IntegerField()
    time = models.TimeField()