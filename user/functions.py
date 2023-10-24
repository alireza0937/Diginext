import random
import re


def generate_otp():
    random_5_digit_number = random.randint(10000, 99999)
    return random_5_digit_number


class GenerateOTP:
    def __init__(self):
        ...


def validate_username_and_password(username, password):
    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$'
    username_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\s]*$'
    return bool(re.match(password_pattern, password) and re.match(username_pattern, username))


def validate_phone_number(phone_number):
    pattern = r'^0\d{10}$'
    return bool(re.match(pattern, phone_number))


def validata_company_name(company_name):
    pattern = r'^[\u0600-\u06FF\s]+$'
    response = re.match(pattern, company_name) is not None
    return response



