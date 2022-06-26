from django.db.models import Count

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter

from flight_tracking_app.flights.api.serializers import AirportSerializer, FlightSerializer
from flight_tracking_app.flights.models import Airport, Flight


class AirportViewSet(ModelViewSet):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()
    lookup_url_kwarg = 'code'


class FlightViewSet(ModelViewSet):
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()

    def get_queryset(self):
        queryset = Flight.objects.all()
        return self.get_serializer_class().setup_eager_loading(queryset)

    @extend_schema(
        description='Return total flight counts based on flight number.',
        methods=["GET"],
        parameters=[
            OpenApiParameter(name='flight_number', description='Filter by flight number', required=True, type=str),
        ]
    )
    @action(detail=False, methods=['GET'], url_name='total-flights')
    def total_flights(self, request):
        flight_number = request.GET.get('flight_number')
        flights = (
            Flight.objects
            .filter(flight_number=flight_number)
            .values('flight_number')
            .annotate(count=Count('id'))
        )
        return Response(status=status.HTTP_200_OK, data=flights)
