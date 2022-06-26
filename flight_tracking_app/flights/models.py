from django.db import models


class Airport(models.Model):
    code = models.CharField(max_length=10, primary_key=True, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.code} - {self.name}'


class Flight(models.Model):
    flight_number = models.CharField(max_length=25, db_index=True)
    origin = models.ForeignKey(to=Airport, related_name='flights_origin', on_delete=models.CASCADE)
    destination = models.ForeignKey(to=Airport, related_name='flights_destination', on_delete=models.CASCADE)
    take_off = models.DateTimeField()
    landing = models.DateTimeField()

    def __str__(self):
        return self.flight_number
