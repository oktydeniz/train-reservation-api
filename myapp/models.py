from django.db import models


class Wagon(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    occupied_seats = models.IntegerField()


class Train(models.Model):
    name = models.CharField(max_length=100)
    wagons = models.ManyToManyField(Wagon)


class Reservation(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    num_of_people = models.IntegerField()
    allow_different_wagons = models.BooleanField(default=True)
