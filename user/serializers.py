from rest_framework import serializers


class FirstStepRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.IntegerField(required=True)


class SecondStepRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField(required=True)


class ThirdStepRegistrationSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required=True)
    cars = serializers.IntegerField(required=True)
    company_name = serializers.CharField(required=True)



