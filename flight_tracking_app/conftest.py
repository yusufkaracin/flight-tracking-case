from typing import Callable, List

import pytest
from rest_framework.test import APIClient

from flight_tracking_app.flights.models import Airport, Flight
from flight_tracking_app.flights.tests.factories import AirportFactory, FlightFactory


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def create_airport() -> Callable:
    def _create_airport(count: int) -> List[Airport]:
        result = []

        for i in range(count):
            result.append(AirportFactory())

        return result

    return _create_airport


@pytest.fixture
def create_flight() -> Callable:
    def _create_flight(count: int, flight_numbers=None) -> List[Flight]:
        result = []

        for i in range(count):
            params = {}

            if flight_numbers:
                params['flight_number'] = flight_numbers[i]

            result.append(FlightFactory(**params))

        return result

    return _create_flight
