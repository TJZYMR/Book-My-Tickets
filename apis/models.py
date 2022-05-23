from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        password=None,
        is_admin=False,
        is_staff=False,
        is_active=True,
    ):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email), password=password)

        user.set_password(password)  # change password to hash
        user.is_admin = is_admin
        user.is_staff = is_staff
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.create_user(email=self.normalize_email(email), password=password)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    address = models.TextField(max_length=200, default=" ")
    contact = models.CharField(max_length=15, default=" ")
    gender = models.CharField(max_length=100, default=" ")
    city = models.CharField(max_length=200, default=" ")
    age = models.CharField(max_length=100, default=" ")
    state = models.CharField(max_length=200, default=" ")
    country = models.CharField(max_length=200, default=" ")
    pincode = models.CharField(max_length=20, default=" ")
    date_of_birth = models.DateTimeField(null=True)
    permission = models.CharField(max_length=200, default=" ")
    # date_joined = None
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def isAdmin(self):
        if self.permission == "admin":
            return True
        else:
            return False

    def __str__(self):
        return self.name


class Passenger(models.Model):
    aadharno = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    telephone_number = models.CharField(max_length=15)
    emailid = models.EmailField(max_length=200)
    gender = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class FlightDetails(models.Model):
    flight_name = models.CharField(max_length=200)
    airline_name = models.CharField(max_length=200)
    source_airport = models.CharField(max_length=200)
    destination_airport = models.CharField(max_length=200)
    source_state = models.CharField(
        max_length=200
    )  # source-state_name or source_countru
    destination_state = models.CharField(
        max_length=200
    )  # destination_state or destination_country

    flight_duration = models.CharField(max_length=200)
    stops = models.CharField(max_length=200)
    arrival_time = models.DateTimeField(auto_now_add=False)
    departure_time = models.DateTimeField(auto_now_add=False)

    remaining_seats = (
        models.IntegerField()
    )  # Q.1=>does django implicitly convert this charfield to number.
    total_seats = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)

    def __str__(self):
        return self.flight_name


class Book(models.Model):
    # booking_number = models.CharField(max_length=200)
    # pnr = models.CharField(max_length=200)
    booking_date = models.DateField(auto_now=True)
    trip_date = models.DateField()
    num_of_passengers = models.CharField(max_length=200)
    total_price = models.CharField(max_length=200)
    booking_time = models.TimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(FlightDetails, on_delete=models.CASCADE)
    passenger = models.ManyToManyField(Passenger)

    def __str__(self):
        return self.user.name + "(" + str(self.id) + ")"
