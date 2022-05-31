from pyparsing import Token
from apis.models import FlightDetails, User, Airport, Book
from apis.models import User
from django.urls import reverse
from django.test import TestCase, Client

from rest_framework import status
from rest_framework.test import APITestCase
from http.cookies import SimpleCookie
from django.test import RequestFactory


class TestAirportModel(TestCase):

    # Things to test:
    # - Can be create a post with the bare minimum of fields? (Title, body and author)
    # - Does the __str__ method behave as expected?
    # - Is a slug automatically created?
    # - Do two posts with the same title and user get different slugs?

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="janedoe@test.com",
            password="password456",
        )
        cls.airport = Airport.objects.create(name="sds", country="india")
        cls.flight = FlightDetails.objects.create(
            flight_name="tj",
            arrival_time="2022-05-19 11:46:05",
            departure_time="2022-05-19 09:46:05",
            remaining_seats="10",
            airport=cls.airport,
        )
        cls.book = Book.objects.create(
            num_of_passengers="2",
            total_price="1233",
            trip_date="2022-05-23",
            flight=cls.flight,
            user=cls.user,
        )
        # cls.url = reverse(LoginView)
        cls.url1 = "/api/v1/login"

    def test_create_post(self):
        # Tests that a post with a title, body, user and creation date can be created

        self.assertEqual(self.book.num_of_passengers, "2")
        self.assertEqual(self.book.user, self.user)
        self.assertEqual(self.flight.airport, self.airport)

        self.assertEqual(self.book.user, self.user)
        self.assertEqual(self.airport.name, "sds")
        self.assertEqual(self.flight.arrival_time, "2022-05-19 11:46:05")


# def test_post_str(self):
#     # Tests the __str__ of the Post model
#     # self.user.name + ( + str(self.id) + )
#     self.assertEqual(str(self.flight), "tj")

# def test_user_must_be_logged_in(self):
#     # Tests that a non-logged in user is redirected
#     response = self.client.get(self.url)
#     # self.assertEqual(response.status_code, 302)


class TestUserModel(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = "/api/v1/login"
        cls.urls = "/api/v1/user"
        cls.url1 = "/api/v1/register"
        cls.url2 = "/api/v1/flight_details"
        cls.user = User.objects.create_user(email="t@gmail.com", password="t")

    def test_login(self):
        self.client.force_login(self.user)
        form_data = {
            "email": "t@gmail.com",
            "password": "t",
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_flightdetails(self):
        # self.client.force_login(self.user)

        # form_data = {
        #     "id": 1,
        #     "flight_name": "jalag",
        #     "airline_name": "indigo",
        #     "source_airport": "AMD",
        #     "destination_airport": "DLH",
        #     "source_state": "gujarat",
        #     "destination_state": "delhi",
        #     "flight_duration": "2 hrs",
        #     "stops": "0",
        #     "arrival_time": "2022-05-19T11:46:05Z",
        #     "departure_time": "2022-05-19T09:46:05Z",
        #     "remaining_seats": 22,
        #     "total_seats": "80",
        #     "price": "5000",
        #     "airport": 1,
        # }
        response = self.client.get(self.url2)
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.username = "usuario"
        self.password = "contrasegna"
        self.data = {"email": "usuario@mail.com", "password": self.password}

    def test_token_auth(self):

        # URL using path name
        # url = reverse("login")

        # Create a user is a workaround in order to authentication works
        user = User.objects.create_user(
            email="usuario@mail.com", password="contrasegna"
        )
        self.assertEqual(user.is_active, 1, "Active User")

        # First post to get token
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        token = response.data["token"]

        response = self.client.get(self.url2, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.cookies = SimpleCookie({"token": token})
        response = self.client.get(self.url2)
        # print(response)
        self.assertEqual(response.status_code, 200)

        # response = self.client.post(self.url2, format="json")
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(token)
        # request = RequestFactory().get(self.url2)
        # request.COOKIES["token"] = token
        # response = self.client.post(request, data={"format": "json"})
        # self.assertEqual(response.status_code, status.HTTP_200_OK)


# Next post/get's will require the token to connect
# self.client.credentials(HTTP_AUTHORIZATION="Token {0}".format(token))
# print(f"JWT token: {token}")
# response = self.client.get(self.urls, data={"format": "json"})
# self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
