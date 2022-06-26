from rest_framework.routers import SimpleRouter

from flight_tracking_app.flights.api.views import AirportViewSet, FlightViewSet

app_name = "api"
router = SimpleRouter()
router.register("airports", AirportViewSet)
router.register("flights", FlightViewSet)
urlpatterns = router.urls
