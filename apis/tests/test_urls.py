from pydoc import resolve
from django.test import SimpleTestCase

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apis.views import (
    PassengerViewSet,
    AirportViewSet,
    UserView,
    RegisterView,
    LoginView,
    BookViewSet,
    FlightDetailsViewSet,
)


class TestUrls(SimpleTestCase):
    def test_testhomepage(self):
        response = self.client.get("/api/v1/airports")
        self.assertEqual(response.status_code, 200)
