import random
import re
import redis
from django.http import HttpRequest
from rest_framework.authtoken.models import Token
from user.models import User, Company


def generate_otp():
    random_5_digit_number = random.randint(10000, 99999)
    return random_5_digit_number


def validate_username_and_password(username, password):
    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$'
    username_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\s]*$'
    return bool(re.match(password_pattern, password) and re.match(username_pattern, username))


def validate_phone_number(phone_number):
    pattern = r'^0\d{10}$'
    return bool(re.match(pattern, phone_number))


def create_user(username, password):
    User.objects.create_user(username=username, password=password)
    user = User.objects.get(username=username)
    token, created = Token.objects.get_or_create(user=user)
    return token


def connect_to_redis_and_retrieve_info(user_information, phone_number):
    connection = create_redis_connection()
    if connection.get(user_information) is None and connection.get(
            f"{user_information}_timelimit") is None:
        otp = generate_otp()
        connection.setex(user_information, 120, otp)
        connection.setex(f"{user_information}_timelimit", 300, otp)
        connection.setex(f"{user_information}_phone", 120, phone_number)
        return True, otp
    return False


def get_user_id(token):
    user_information = Token.objects.get(key=token).user.id
    user = User.objects.filter(id=user_information).first()
    return user, user_information


def get_token_from_request(request: HttpRequest):
    authorization_header = request.headers.get('Authorization')
    token = authorization_header.split(' ')[1]
    return token


def get_user_id_from_token(token):
    user = Token.objects.get(key=token).user
    return user.id


def create_redis_connection():
    return redis.Redis(host='localhost', port=6379, decode_responses=True)


def get_otp_from_redis(connection, user_id):
    return connection.get(user_id)


def validate_otp(request, otp):
    insert_otp = request.POST.get('otp')
    return int(otp) == int(insert_otp)


def validate_company_name(company_name):
    pattern = r'^[\u0600-\u06FF\s]+$'
    response = re.match(pattern, company_name) is not None
    return response


def update_user_profile(request, user_id, connection):
    number_of_cars = request.POST.get("cars")
    company_name = request.POST.get("company_name")

    if not validate_company_name(company_name):
        return False

    user = User.objects.filter(id=user_id).first()
    Company(user=user, company_name=company_name, number_of_cars=number_of_cars)
    user.phone_number = connection.get(f'{user_id}_phone')
    user.is_active = True
    user.save()
    return True
