from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from flight_tracking_app.flights.models import Airport, Flight


class AirportFactory(DjangoModelFactory):
    code = Faker('bothify', text='???##')
    name = Faker("name")

    class Meta:
        model = Airport


class FlightFactory(DjangoModelFactory):
    flight_number = Faker('bothify', text='?????##')
    origin = SubFactory(AirportFactory)
    destination = SubFactory(AirportFactory)
    take_off = Faker('date_time')
    landing = Faker('date_time')

    class Meta:
        model = Flight
