from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from .functions import *
from .redis_connection import redis_connection
from .serializers import FirstStepRegistrationSerializer, SecondStepRegistrationSerializer, \
    ThirdStepRegistrationSerializer


class FirstStepRegistration(APIView):
    authentication_classes = [TokenAuthentication]

    @extend_schema(request=FirstStepRegistrationSerializer)
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            serializer = FirstStepRegistrationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"message": "Inserted username or password is not valid."},
                                status=status.HTTP_400_BAD_REQUEST)

            user_exists = User.objects.filter(username=username).exists()

            if not user_exists:
                token = create_user(username=username, password=password)
                return Response({"message": "Successfully", "Authentication Token": token.key})

            return Response({'message': 'Username already exists.'}, status=status.HTTP_409_CONFLICT)
        except:
            return Response({"message": "The entered information is not complete"}, status=status.HTTP_400_BAD_REQUEST)


class SecondStepRegistration(APIView):
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
                if redis_connection.get_key(user.pk) is None and redis_connection.get_key(f"{user.pk}_timelimit") is None:
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


class ThirdStepRegistration(APIView):
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
                    if create_company_profile(number_of_cars, company_name, user, redis_connection):
                        return Response({"message": "Account activated successfully"})
                    return Response({"message": "The entered information is not complete"})

                return Response({"message": "Wrong OTP"})
            return Response({"message": "The company name should only contains persian character."})
        except:
            return Response({"message": "The entered information is not complete"}, status=status.HTTP_400_BAD_REQUEST)


class State(APIView):

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
