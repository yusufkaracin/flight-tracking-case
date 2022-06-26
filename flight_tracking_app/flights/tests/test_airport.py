from typing import Callable

from django.urls import reverse

import pytest
from rest_framework.test import APIClient
from rest_framework import status

from flight_tracking_app.flights.models import Airport


pytestmark = pytest.mark.django_db


def test_airport_list(api_client: APIClient, create_airport: Callable):
    airport_count = 5
    url = reverse("api:airport-list")
    create_airport(airport_count)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == airport_count


def test_airport_detail(api_client: APIClient, create_airport: Callable):
    airport_count = 3
    airport = create_airport(airport_count)[0]
    url = reverse("api:airport-detail", kwargs={'code': airport.code})

    response = api_client.get(url)
    res_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert res_json['code'] == airport.code


def test_airport_create_success(api_client: APIClient, db):
    url = reverse("api:airport-list")
    payload = {
        'code': 'abc123',
        'name': 'airport test'
    }

    response = api_client.post(url, data=payload)
    res_json = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert res_json['code'] == payload['code']
    assert Airport.objects.count() == 1


def test_airport_create_fail(api_client: APIClient, db):
    url = reverse("api:airport-list")
    payload = {
        'name': 'airport test'
    }

    response = api_client.post(url, data=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Airport.objects.count() == 0


def test_airport_delete(api_client: APIClient, db, create_airport: Callable):
    airport_count = 3
    airport = create_airport(airport_count)[0]
    url = reverse("api:airport-detail", kwargs={'code': airport.code})

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Airport.objects.count() == airport_count - 1
