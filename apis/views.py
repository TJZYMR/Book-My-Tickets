from asyncio.windows_events import NULL
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from apis.auth import authenticateusingcookie
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from .serializers import (
    UserSerializer,
    PassengerSerializers,
    FlightDetailsSerializers,
    AirportSerializers,
    BookSerializers,
)


# from rest_framework import HTTP_HEADER_ENCODING, exceptions

# from .authenticate import TokenAuthSupportCookie
from rest_framework import routers, serializers, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from .models import User, Passenger, FlightDetails, Airport, Book
from rest_framework import filters
from rest_framework import status
from django.http import JsonResponse
from django_filters import rest_framework as filters
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from .auth import authenticateusingcookie, authorizationusingcookie

# from django.contrib.auth.models import User

# from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import permissions

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256").decode("utf-8")

        response = Response()

        response.set_cookie(key="token", value=token, httponly=True)
        response.data = {"token": token}
        return response


class UserView(APIView):
    def get(self, request):
        # token = request.COOKIES.get("token")

        # if not token:
        #     raise AuthenticationFailed("Unauthenticated!")

        # try:
        #     payload = jwt.decode(token, "secret", algorithm=["HS256"])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed("Unauthenticated!")
        payload = authenticateusingcookie(request)
        data1 = authorizationusingcookie(payload123=payload)
        # user = User.objects.filter(id=payload["id"]).first()
        # serializer = UserSerializer(user)
        return Response(data1.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("token")
        response.data = {"message": "success"}
        return response


class PassengerViewSet(viewsets.ModelViewSet):
    serializer_class = PassengerSerializers

    def get_queryset(self):
        passenger = Passenger.objects.all()
        return passenger


class FlightDetailsViewSet(viewsets.ModelViewSet):
    queryset = FlightDetails.objects.all()
    serializer_class = FlightDetailsSerializers
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = [
        "flight_name",
        "airline_name",
        "source_airport",
        "departure_time",
        "airport",
    ]


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializers
    # authentication_classes = [TokenAuthSupportCookie]
    # permission_classes = [AllowAny | ReadOnly]
    # permission_classes = [IsAuthenticated | IsAdminUser]
    def list(self, request):
        payload = authenticateusingcookie(request)
        data1 = authorizationusingcookie(payload123=payload)
        # user = User.objects.filter(id=payload["id"]).first()
        # serializer = UserSerializer(user)
        return Response(data1.data)
        # token = request.COOKIES.get("token")

        # if not token:
        #     raise AuthenticationFailed("Unauthenticated!")

        # try:
        #     payload = jwt.decode(token, "secret", algorithm=["HS256"])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed("Unauthenticated!")

        # user = User.objects.filter(id=payload["id"]).first()
        # if user.isAdmin == "admin":
        #     serializer = UserSerializer(user)
        #     return Response(serializer.data)
        # else:
        #     raise AuthenticationFailed("Not authorized!")


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializers
    # authentication_classes = [TokenAuthSupportCookie]
    # permission_classes = [AllowAny | ReadOnly]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self, request):

        payload = authenticateusingcookie(request)

        books = Book.objects.filter(id=payload["id"]).first()
        if books:
            book = Book.objects.all()
            return book
        else:
            raise AuthenticationFailed("Sorry,User not found!")

    def list(self, request):
        # token = request.COOKIES.get("token")

        # if not token:
        #     raise AuthenticationFailed("Unauthenticated!")

        # try:
        #     payload = jwt.decode(token, "secret", algorithm=["HS256"])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed("Unauthenticated!")

        # user = User.objects.filter(id=payload["id"]).first()
        # if user.isAdmin:
        #     serializer = UserSerializer(user)
        #     return Response(serializer.data)
        # else:
        #     raise AuthenticationFailed("Not authorized!")

        payload = authenticateusingcookie(request)
        data1 = authorizationusingcookie(payload123=payload)
        # user = User.objects.filter(id=payload["id"]).first()
        # serializer = UserSerializer(user)
        return Response(data1.data)

    def create(self, request, *args, **kwargs):

        payload = authenticateusingcookie(request)
        books = Book.objects.filter(pk=payload["id"]).first()
        if books is not NULL:
            data = request.data
            user = User.objects.get(id=data["user"])
            flightdetails = FlightDetails.objects.get(id=data["flight"])
            if len(data["passengers"]) == data["num_of_passengers"]:
                if flightdetails.remaining_seats > int(data["num_of_passengers"]) + 1:
                    new_book = Book.objects.create(
                        # booking_date=data["booking_date"],
                        trip_date=data["trip_date"],
                        num_of_passengers=data["num_of_passengers"],
                        total_price=data["total_price"],
                        user=user,
                        flight=flightdetails,
                    )
                    new_book.save()
                    # print(len(data["passengers"]))
                    for passenger in data["passengers"]:

                        p = Passenger.objects.create(
                            aadharno=passenger["aadharno"],
                            name=passenger["name"],
                            address=passenger["address"],
                            telephone_number=passenger["telephone_number"],
                            emailid=passenger["emailid"],
                            gender=passenger["gender"],
                            age=passenger["age"],
                            user=User.objects.get(id=data["user"]),
                        )
                        new_book.passenger.add(p)
                        updated_remaining_Seats = (
                            flightdetails.remaining_seats
                            - int(data["num_of_passengers"])
                            - 1
                        )
                        FlightDetails.objects.filter(pk=flightdetails.pk).update(
                            remaining_seats=updated_remaining_Seats
                        )
                else:
                    return JsonResponse(
                        {
                            "Message": "Oops!!SOrry seats not available",
                            "status": status.HTTP_403_FORBIDDEN,
                        }
                    )
            else:
                return JsonResponse(
                    {
                        "Message": "Oops!!not all Passengers detail were Given",
                        "status": status.HTTP_403_FORBIDDEN,
                    }
                )

            serializers = BookSerializers(new_book)
            return Response(serializers.data)
        else:
            raise AuthenticationFailed("Sorry,User not found!")
