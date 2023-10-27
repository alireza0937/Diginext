from drf_spectacular.utils import extend_schema
from redis import Redis
from rest_framework.authtoken.models import Token
from django.http import HttpRequest, JsonResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from user.models import User, Company
from .functions import generate_otp, validate_username_and_password, validate_phone_number, validata_company_name
from .serializers import FirstStepRegistrationSerializer, SecondStepRegistrationSerializer, \
    ThirdStepRegistrationSerializer
import redis
import re


def create_user(username, password):
    User.objects.create_user(username=username, password=password)
    user = User.objects.get(username=username)
    token, created = Token.objects.get_or_create(user=user)
    return token


def connect_to_redis_and_retrieve_info(user_information, phone_number):
    connection = redis.Redis(host='localhost', port=6379, decode_responses=True)
    if connection.get(user_information) is None and connection.get(
            f"{user_information}_timelimit") is None:
        otp = generate_otp()
        connection.setex(user_information, 120, otp)
        connection.setex(f"{user_information}_timelimit", 300, otp)
        connection.setex(f"{user_information}_phone", 120, phone_number)
        return True, otp
    return JsonResponse({"message": "Can't request otp for 5 minutes."})


def get_user_id(token):
    user_information = Token.objects.get(key=token).user.id
    user = User.objects.filter(id=user_information).first()
    return user, user_information


class FirstStepRegistration(APIView):
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        request=FirstStepRegistrationSerializer
    )
    def post(self, request: HttpRequest):
        username = request.POST.get('username')
        password = request.POST.get('password')
        validation = validate_username_and_password(username, password)
        if validation:
            user_exists: bool = User.objects.filter(username=username).exists()
            if user_exists is False:
                token = create_user(username=username, password=password)
                return JsonResponse({"message": "Successfully",
                                     "Authentication Token": token.key})

            return JsonResponse({'message': 'Username already exist..'}, status=status.HTTP_409_CONFLICT)
        return JsonResponse({"message": "Inserted username or password is not valid.."},
                            status=status.HTTP_400_BAD_REQUEST)


class SecondStepRegistration(APIView):
    @extend_schema(
        request=SecondStepRegistrationSerializer
    )
    def post(self, request: HttpRequest):
        phone_number = request.POST.get("phone_number")
        token = request.headers.get('Authorization').split(' ')[1]
        validation = validate_phone_number(phone_number)
        if validation:
            user, user_information = get_user_id(token=token)
            if user is not None or user.phone_number == phone_number:
                response, otp = connect_to_redis_and_retrieve_info(user_information, phone_number)
                if response:
                    return JsonResponse({"message": "Phone number set successfully.",
                                         "otp": otp})

            return JsonResponse({"message": "Phone number exists."})
        return JsonResponse({"message": "Phone number is not correct..."})


class ThirdStepRegistration(APIView):
    @extend_schema(request=ThirdStepRegistrationSerializer)
    def post(self, request: HttpRequest):
        try:
            token = self.get_token_from_request(request)
            user_id = self.get_user_id_from_token(token)
            connection = self.create_redis_connection()
            otp = self.get_otp_from_redis(connection, user_id)

            if otp is None:
                return JsonResponse({"message": "The OTP has expired. Please request OTP again"})

            if self.validate_otp(request, otp):
                if self.update_user_profile(request, user_id, connection):
                    return JsonResponse({"message": "Account activated successfully"})
                else:
                    return JsonResponse({"message": "Failed to update user profile"})
            else:
                return JsonResponse({"message": "Wrong OTP"})
        except Exception as e:
            return JsonResponse({"message": str(e)})

    def get_token_from_request(self, request: HttpRequest):
        authorization_header = request.headers.get('Authorization')
        token = authorization_header.split(' ')[1]
        return token

    def get_user_id_from_token(self, token):
        user = Token.objects.get(key=token).user
        return user.id

    def create_redis_connection(self):
        return redis.Redis(host='localhost', port=6379, decode_responses=True)

    def get_otp_from_redis(self, connection, user_id):
        return connection.get(user_id)

    def validate_otp(self, request, otp):
        insert_otp = request.POST.get('otp')
        return int(otp) == int(insert_otp)

    def update_user_profile(self, request, user_id, connection):
        number_of_cars = request.POST.get("cars")
        company_name = request.POST.get("company_name")

        if not self.validate_company_name(company_name):
            return False

        user = User.objects.filter(id=user_id).first()
        Company(user=user_id, company_name=company_name, number_of_cars=number_of_cars).save()
        user.phone_number = connection.get(f'{user_id}_phone')
        user.is_active = True
        user.save()

        return True

    def validate_company_name(self, company_name):
        pattern = r'^[\u0600-\u06FF\s]+$'
        response = re.match(pattern, company_name) is not None
        return response


class State(APIView):
    def post(self, request: HttpRequest):
        try:
            token = request.headers.get('Authorization').split(" ")[1]
            user_id = Token.objects.get(key=token).user.id
        except:
            return JsonResponse({"message": "User not Found.."})
        else:
            user = User.objects.filter(id=user_id).first()
            connection = Redis(host='localhost', port=6379, decode_responses=True)
            if user.phone_number is None:
                return JsonResponse({"message": "You Should insert your phone number"})
            elif user.is_active is True:
                return JsonResponse({"message": "Account already activated.."})
            elif connection.get(user_id):
                return JsonResponse({"message": "You should enter your otp and after that your information such as "
                                                "company name and number of your cars. "})
