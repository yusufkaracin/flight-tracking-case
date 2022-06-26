from django.contrib import admin

from flight_tracking_app.flights.models import Airport, Flight


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    pass


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'origin', 'destination', 'take_off', 'landing')
