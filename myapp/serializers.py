from abc import ABC

from rest_framework import serializers
from .models import Train, Wagon, Reservation


class WagonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wagon
        fields = ['name', 'capacity', 'occupied_seats']


class TrainSerializer(serializers.ModelSerializer):
    wagons = WagonSerializer(many=True)

    class Meta:
        model = Train
        fields = ['name', 'wagons']


class ReservationSerializer(serializers.Serializer):
    train = TrainSerializer()
    num_of_people = serializers.IntegerField()
    allow_different_wagons = serializers.BooleanField()
