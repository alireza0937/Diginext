from string import digits, ascii_letters
import random
import re


def generate_otp():
    random_5_digit_number = random.randint(10000, 99999)
    return random_5_digit_number


def validate_username_and_password(username, password):
    if digits in username or ascii_letters in username or '' in username:
        pattern = r'^(?=.*[A-Z])(?=.*[a-z]).*$'
        return bool(re.match(pattern, password)) and len(password) > 8
    return False


def validate_phone_number(phone_number):
    try:
        int(phone_number)
    except:
        return False
    else:
        if len(str(phone_number)) == 8:
            return True


def validata_company_name(company_name):
    pattern = r'^[\u0600-\u06FF\s]+$'
    response = re.match(pattern, company_name) is not None
    return response


