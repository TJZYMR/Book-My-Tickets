from rest_framework import serializers
from .models import User, Passenger, FlightDetails, Airport, Book


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class AirportSerializers(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class FlightDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = FlightDetails
        fields = "__all__"


class PassengerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        depth = 1
