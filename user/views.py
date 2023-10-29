from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from .functions import *
from .serializers import FirstStepRegistrationSerializer, SecondStepRegistrationSerializer, \
    ThirdStepRegistrationSerializer


class FirstStepRegistration(APIView):
    authentication_classes = [TokenAuthentication]

    @extend_schema(request=FirstStepRegistrationSerializer)
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if not validate_username_and_password(username, password):
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
            authorization_header = request.headers.get('Authorization')
            token = authorization_header.split(' ')[1] if authorization_header else None

            if not phone_number or not validate_phone_number(phone_number):
                return Response({"message": "Phone number is not correct..."}, status=status.HTTP_400_BAD_REQUEST)

            user, user_information = get_user_id(token=token)

            if user is not None or user.phone_number == phone_number:
                try:
                    response, otp = connect_to_redis_and_retrieve_info(user_information, phone_number)
                    return Response({"message": "Phone number set successfully.", "otp": otp})
                except:
                    return Response({"message": "Can't request OTP for 5 minutes."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Phone number exists."}, status=status.HTTP_409_CONFLICT)
        except:
            return Response({"message": "The entered information is not complete"}, status=status.HTTP_400_BAD_REQUEST)


class ThirdStepRegistration(APIView):
    @extend_schema(request=ThirdStepRegistrationSerializer)
    def post(self, request):
        try:
            token = get_token_from_request(request)
            user_id = get_user_id_from_token(token)
            connection = create_redis_connection()
            otp = get_otp_from_redis(connection, user_id)

            if otp is None:
                return Response({"message": "The OTP has expired. Please request OTP again"})

            if validate_otp(request, otp):
                if update_user_profile(request, user_id, connection):
                    return Response({"message": "Account activated successfully"})
                return Response({"message": "Failed to update user profile"})

            return Response({"message": "Wrong OTP"})

        except Exception as e:
            return Response({"message": "The entered information is not complete"}, status=status.HTTP_400_BAD_REQUEST)


class State(APIView):

    def post(self, request):
        try:
            token = request.headers.get('Authorization').split(" ")[1]
            user_id = Token.objects.get(key=token).user.id
        except Token.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(id=user_id).first()
        connection = create_redis_connection()

        if user.phone_number is None:
            return Response({"message": "You should insert your phone number."}, status=status.HTTP_400_BAD_REQUEST)
        elif user.is_active:
            return Response({"message": "Account already activated."}, status=status.HTTP_200_OK)
        elif connection.get(user_id):
            return Response({"message": "You should enter your OTP and then provide additional information."},
                            status=status.HTTP_200_OK)
