from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from redis_connection import redis_connection
from user.functions import generate_otp
from user.serializers.SecondStepRegistrationSerializer import SecondStepRegistrationSerializer


class SecondStepRegistrationAPIView(APIView):
    @extend_schema(request=SecondStepRegistrationSerializer)
    def post(self, request):
        try:
            phone_number = request.data.get("phone_number")
            user = request.META.get("user")
            serializer = SecondStepRegistrationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"message": "Phone number is not correct or is duplicate ..."},
                                status=status.HTTP_400_BAD_REQUEST)
            if user is not None or user.phone_number == phone_number:
                if redis_connection.get_key(user.pk) is None and redis_connection.get_key(
                        f"{user.pk}_timelimit") is None:
                    otp = generate_otp()
                    redis_connection.setex_key(user.pk, 120, otp)
                    redis_connection.setex_key(f"{user.pk}_timelimit", 300, otp)
                    redis_connection.setex_key(f"{user.pk}_phone", 120, phone_number)
                    return Response({"message": "Phone number set successfully.", "otp": otp})

                return Response({"message": "Can't request OTP for 5 minutes."},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Phone number exists."}, status=status.HTTP_409_CONFLICT)
        except:
            return Response({"message": "The entered information is not complete"}, status=status.HTTP_400_BAD_REQUEST)