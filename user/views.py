from drf_spectacular.utils import extend_schema
from redis import Redis
from rest_framework.authtoken.models import Token
from django.http import HttpRequest, JsonResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from user.models import User
from .functions import generate_otp, validate_username_and_password, validate_phone_number, validata_company_name
from .serializers import FirstStepRegistrationSerializer, SecondStepRegistrationSerializer, ThirdStepRegistrationSerializer
import redis


class FirstStepRegistration(APIView):
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        request=FirstStepRegistrationSerializer
    )
    def post(self, request: HttpRequest):
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            validation = validate_username_and_password(username, password)
            if validation:
                user_exists: bool = User.objects.filter(username=username).exists()
                if user_exists is False:
                    User.objects.create_user(username=username, password=password)
                    user = User.objects.get(username=username)
                    token, created = Token.objects.get_or_create(user=user)
                    return JsonResponse({"message": "Successfully",
                                         "Authentication Token": token.key})
            return JsonResponse({'message': 'Username already exist..'}, status=status.HTTP_400_BAD_REQUEST)
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

            user_information = Token.objects.get(key=token).user.id
            user = User.objects.filter(id=user_information).first()
            user2 = User.objects.filter(id=user_information, phone_number=phone_number).first()
            if user is not None or user2 is not None:
                user.phone_number = phone_number
                user.save()
                connection = redis.Redis(host='localhost', port=6379, decode_responses=True)
                if connection.get(user_information) is None and connection.get(
                        f"{user_information}_timelimit") is None:
                    otp = generate_otp()
                    connection.setex(user_information, 240, otp)
                    connection.setex(f"{user_information}_timelimit", 300, otp)
                    return JsonResponse({"message": "Phone number set successfully.",
                                         "otp": otp})
                return JsonResponse({"message": "Can't request otp for 5 minutes."})
            return JsonResponse({"message": "Phone number exists."})
        return JsonResponse({"message": "Phone number is not correct..."})


class ThirdStepRegistration(APIView):
    @extend_schema(
        request=ThirdStepRegistrationSerializer
    )
    def post(self, request: HttpRequest):
        token = request.headers.get('Authorization').split(' ')[1]
        insert_otp = request.POST.get('otp')
        connection = redis.Redis(host='localhost', port=6379, decode_responses=True)
        user_id = Token.objects.get(key=token).user.id
        otp = connection.get(user_id)
        if otp is None:
            return JsonResponse({"message": "The otp has expired,Please request otp again"})
        if int(otp) == int(insert_otp):
            number_of_cars = request.POST.get("cars")
            company_name = request.POST.get("company_name")
            validation = validata_company_name(company_name)
            if validation:
                user = User.objects.filter(id=user_id).first()
                user.number_of_cars = number_of_cars
                user.company_name = company_name
                user.is_active = True
                user.save()
                return JsonResponse({"message": "Account activated successfully"})
            else:
                return JsonResponse({"message": "Company name is incorrect."})
        else:
            return JsonResponse({"message": "Wrong Token."})


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
