import re
from django.db import models

# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    def get_distribution(self) -> list:
        distribution = [
            [True, True]
            for v in range(0, int(self.passengers / 2))
        ]

        if self.passengers % 2 != 0:
            distribution.append([True, False])

        return distribution


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    def finished(self, end) -> None:
        self.end = end
        self.save()

    def is_finished(self) -> bool:
        return self.end is not None


def validate_number_plate(number_plate: str) -> bool:
    return re.search('[A-Z]{2}-[0-9]{2}-[0-9]{2}', number_plate) is not None
