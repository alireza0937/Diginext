from rest_framework import serializers, status
import re

from rest_framework.response import Response

from user.models import User


class FirstStepRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_password(self, password):
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$'
        if bool(re.match(password_pattern, password)):
            return password

    def validate_username(self, username):
        username_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\s]*$'
        if bool(re.match(username_pattern, username)):
            return username


class SecondStepRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    def validate_phone_number(self, phone_number):
        pattern = r'^0\d{10}$'
        phone_number_exists: bool = User.objects.filter(phone_number=phone_number).exists()
        response = bool(re.match(pattern, str(phone_number)) and not phone_number_exists)
        if response:
            return True
        raise serializers.ValidationError("Invalid phone number format")





class ThirdStepRegistrationSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required=True)
    cars = serializers.IntegerField(required=True)
    company_name = serializers.CharField(required=True)

    def validate_company_name(self, company_name):
        pattern = r'^[\u0600-\u06FF\s]+$'
        response = re.match(pattern, company_name) is not None
        return response
