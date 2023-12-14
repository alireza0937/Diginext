import codecs
import random
from rest_framework.authtoken.models import Token
from user.models import User, Company


def generate_otp():
    random_5_digit_number = random.randint(10000, 99999)
    return random_5_digit_number


def create_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    token, created = Token.objects.get_or_create(user=user)
    return token


def validate_otp(insert_otp, otp):
    return int(otp) == int(insert_otp)


def complete_creation_profile(number_of_cars, company_name, user, connection):
    Company.objects.create(user=user, company_name=company_name, number_of_cars=number_of_cars)
    phone_number = connection.get_key(f'{user.pk}_phone')
    phone_number = codecs.decode(phone_number, 'utf-8')
    user.phone_number = phone_number
    user.is_active = True
    user.save()
    return True

