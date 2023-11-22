from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from redis_connection import redis_connection
from user.functions import validate_otp, complete_creation_profile
from user.serializers.ThirdStepRegistrationSerializer import ThirdStepRegistrationSerializer


class ThirdStepRegistrationAPIView(APIView):
    @extend_schema(request=ThirdStepRegistrationSerializer)
    def post(self, request):
        try:
            user = request.META.get("user")
            otp = redis_connection.get_key(user.pk)
            insert_otp = request.data.get('otp')
            number_of_cars = request.data.get("cars")
            company_name = request.data.get("company_name")
            serializer = ThirdStepRegistrationSerializer(data=request.data)

            if otp is None:
                return Response({"message": "The OTP has expired. Please request OTP again"})

            if serializer.is_valid():
                if validate_otp(insert_otp, otp):
                    if complete_creation_profile(number_of_cars, company_name, user, redis_connection):
                        return Response({"message": "Account activated successfully"})
                    return Response({"message": "The entered information is not complete"})

                return Response({"message": "Wrong OTP"})
            return Response({"message": "The company name should only contains persian character."})
        except:
            return Response({"message": "The entered information is not complete"}, status=status.HTTP_400_BAD_REQUEST)