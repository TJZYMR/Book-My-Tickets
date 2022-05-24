from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .serializers import UserSerializer
import jwt


def authenticateusingcookie(request):
    token = request.COOKIES.get("token")

    if not token:
        raise AuthenticationFailed("Unauthenticated!")

    try:
        payload = jwt.decode(token, "secret", algorithm=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated!")


def authorizationusingcookie(payload123):
    user = User.objects.filter(id=payload123["id"]).first()
    if user.isAdmin:
        serializer = UserSerializer(user)
        return serializer
    else:
        raise AuthenticationFailed("Not authorized!")
