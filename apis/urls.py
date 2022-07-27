from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView
from rest_framework.routers import DefaultRouter


from .views import (
    PassengerViewSet,
    FlightDetailsViewSet,
    AirportViewSet,
    BookViewSet,
    FlightDetailsViewSetwithslug,
)

urlpatterns = [
    path("register", RegisterView.as_view(), name="reg"),
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
    path(  # Post allowed only by superuser and Get Allowed for all
        "airports", AirportViewSet.as_view({"get": "list"})
    ),  # Any user can view this,but only superuser can modify the Database
    path(  # Post allowed only by authenticated user and Get Allowed for authenticated user only
        "user", UserView.as_view()
    ),  # Authenticated user can view the profile details of self.
    path(  # Post and Get Allowed
        "passengers", PassengerViewSet.as_view({"get": "list"})
    ),  # Only the user who booked the flight can view the passengers associated with that booking and with that User.
    path(  # Post and Get Allowed
        "flight_details",
        FlightDetailsViewSet.as_view({"get": "list", "post": "create"}),
    ),  # Any user can view this,but only superuser can modify the Database
    path(  # Post and Get Allowed
        "flight_details/<int:pk>/",
        FlightDetailsViewSet.as_view({"delete": "destroy"}),
    ),  # Any user can view this,but only superuser can modify the Database
    path(  # Post and Get Allowed
        "flight_details/<str:slug>/",
        FlightDetailsViewSetwithslug.as_view(),
    ),
    path(  # Post and Get Allowed
        "flight_details/<int:pk>/",
        FlightDetailsViewSet.as_view({"put": "update"}),
    ),  # Any user can view this,but only superuser can modify the Database
    path(
        "booking", BookViewSet.as_view({"post": "create", "get": "list"})
    ),  # authentication required before booking
    # Post and Get Allowed
]

# router = DefaultRouter()
# router.register(r"users", UserViewSet, basename="users")
# router.register(r"passengers", PassengerViewSet, basename="passengers")
# router.register(r"flight_details", FlightDetailsViewSet, basename="flight_details")
# router.register(r"airports", AirportViewSet, basename="Airport")
# router.register(r"booking", BookViewSet, basename="book")

# urlpatterns = router.urls
