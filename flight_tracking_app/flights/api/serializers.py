from rest_framework import serializers

from flight_tracking_app.flights.models import Flight, Airport
from flight_tracking_app.utils.mixins import EagerLoadingMixin


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['code', 'name']


class AirportCodeField(serializers.RelatedField):
    def to_internal_value(self, code):
        airport = Airport.objects.filter(code=code).first()

        if not airport:
            raise serializers.ValidationError(f'No airport exists with code {code}')

        return airport

    def to_representation(self, value):
        return value.code


class FlightSerializer(serializers.ModelSerializer, EagerLoadingMixin):
    select_related_fields = ('origin', 'destination')

    class Meta:
        model = Flight
        fields = ['id', 'flight_number', 'take_off', 'landing', 'from', 'to']

    def validate(self, data):
        """
        Check that start is before finish.
        """
        print(data)
        return data


FlightSerializer._declared_fields["to"] = AirportCodeField(source="destination", queryset=Airport.objects.none())
FlightSerializer._declared_fields["from"] = AirportCodeField(source="origin", queryset=Airport.objects.none())
