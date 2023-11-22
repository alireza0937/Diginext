from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from redis_connection import redis_connection
from user.models import User


class StateAPIView(APIView):

    def post(self, request):
        try:
            user = request.META.get("user")
        except Token.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(id=user.pk).first()

        if user.phone_number is None:
            return Response({"message": "You should insert your phone number."}, status=status.HTTP_400_BAD_REQUEST)
        elif user.is_active:
            return Response({"message": "Account already activated."}, status=status.HTTP_200_OK)
        elif redis_connection.get_key(user.pk):
            return Response({"message": "You should enter your OTP and then provide additional information."},
                            status=status.HTTP_200_OK)
