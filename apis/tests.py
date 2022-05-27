from apis.models import FlightDetails, User, Airport, Book
from apis.models import User
from django.urls import reverse
from django.test import TestCase, Client


# class TestAirportModel(TestCase):

#     Things to test:
#     - Can be create a post with the bare minimum of fields? (Title, body and author)
#     - Does the __str__ method behave as expected?
#     - Is a slug automatically created?
#     - Do two posts with the same title and user get different slugs?


#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(
#             email=janedoe@test.com,
#             password=password456,
#         )
#         cls.airport = Airport.objects.create(name=sds, country=india)
#         cls.flight = FlightDetails.objects.create(
#             flight_name=tj,
#             arrival_time=2022-05-19 11:46:05,
#             departure_time=2022-05-19 09:46:05,
#             remaining_seats=10,
#             airport=cls.airport,
#         )
#         cls.book = Book.objects.create(
#             num_of_passengers=2,
#             total_price=1233,
#             trip_date=2022-05-23,
#             flight=cls.flight,
#             user=cls.user,
#         )
#         cls.url = reverse(LoginView)

#     def test_create_post(self):
#         Tests that a post with a title, body, user and creation date can be created

#         self.assertEqual(self.book.num_of_passengers, 2)
#         self.assertEqual(self.book.user, self.user)
#         self.assertEqual(self.flight.airport, self.airport)

#         self.assertEqual(self.book.user, self.user)
#         self.assertEqual(self.airport.name, sds)
#         self.assertEqual(self.flight.arrival_time, 2022-05-19 11:46:05)

#     def test_post_str(self):
#         Tests the __str__ of the Post model
#         # self.user.name + ( + str(self.id) + )
#         self.assertEqual(str(self.flight), tj)

#     def test_user_must_be_logged_in(self):
#         Tests that a non-logged in user is redirected
#         response = self.client.get(self.url)
#         # self.assertEqual(response.status_code, 302)


class TestUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = "/api/v1/login"
        cls.url1 = "/api/v1/register"
        cls.user = User.objects.create_user(email="t@gmail.com", password="t")

    def test_login(self):
        self.client.force_login(self.user)
        form_data = {
            "email": "t@gmail.com",
            "password": "t",
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        self.client.force_login(self.user)
        form_data = {
            "last_login": "2022-05-23T09:43:51Z",
            "is_superuser": True,
            "is_staff": True,
            "is_active": True,
            "date_joined": "2022-05-23T09:41:51.988363Z",
            "name": "kishu Joshi",
            "email": "k@gmail.com",
            "password": "k",
            "address": "Add1",
            "contact": "7987495244",
            "gender": "Male",
            "city": "Ahmedabad",
            "age": "33",
            "state": "Gujarat",
            "country": "India",
            "pincode": "380051",
            "date_of_birth": "2022-05-23T09:42:56Z",
            "permission": "admin",
        }
        response = self.client.post(self.url1, data=form_data)
        self.assertEqual(response.status_code, 201)
