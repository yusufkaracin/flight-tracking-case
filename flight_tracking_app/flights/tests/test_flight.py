from datetime import datetime
from typing import Callable

from django.urls import reverse

import pytest
from rest_framework.test import APIClient
from rest_framework import status

from flight_tracking_app.flights.models import Flight


pytestmark = pytest.mark.django_db


def test_flight_list(api_client: APIClient, create_flight: Callable):
    flight_count = 5
    url = reverse("api:flight-list")
    create_flight(flight_count)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == flight_count


def test_flight_detail(api_client: APIClient, create_flight: Callable):
    flight_count = 3
    flight = create_flight(flight_count)[0]
    url = reverse("api:flight-detail", kwargs={'pk': flight.pk})

    response = api_client.get(url)
    res_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert res_json['flight_number'] == flight.flight_number


def test_flight_create_success(api_client: APIClient, db, create_airport: Callable):
    url = reverse("api:flight-list")
    airport_1, airport_2 = create_airport(2)
    take_off = datetime.now().strftime('%Y-%m-%dT%H:%M:00Z')
    payload = {
        'flight_number': 'abc123',
        'to': airport_1.code,
        'from': airport_2.code,
        'take_off': take_off,
        'landing': take_off,
    }

    response = api_client.post(url, data=payload)
    res_json = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert res_json['flight_number'] == payload['flight_number']
    assert Flight.objects.count() == 1


def test_flight_create_fail(api_client: APIClient, db):
    url = reverse("api:airport-list")
    payload = {}

    response = api_client.post(url, data=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Flight.objects.count() == 0


def test_flight_delete(api_client: APIClient, db, create_flight: Callable):
    flight_count = 3
    flight = create_flight(flight_count)[0]
    url = reverse("api:flight-detail", kwargs={'pk': flight.pk})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Flight.objects.count() == flight_count - 1


def test_total_flight_count(api_client: APIClient, create_flight: Callable):
    flight_number_1 = 'foo'
    flight_number_2 = 'bar'
    flight_numbers = [flight_number_1, flight_number_1, flight_number_1, flight_number_2]
    create_flight(flight_numbers=flight_numbers, count=len(flight_numbers))
    url = reverse("api:flight-total-flights")

    response = api_client.get(url)
    res_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(res_json) == 0

    response = api_client.get(url, data={'flight_number': flight_number_1})
    res_json = response.json()[0]

    assert response.status_code == status.HTTP_200_OK
    assert res_json['flight_number'] == flight_number_1
    assert res_json['count'] == 3

    response = api_client.get(url, data={'flight_number': flight_number_2})
    res_json = response.json()[0]

    assert response.status_code == status.HTTP_200_OK
    assert res_json['flight_number'] == flight_number_2
    assert res_json['count'] == 1
