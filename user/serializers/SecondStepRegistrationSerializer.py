import re
from rest_framework import serializers
from user.models import User


class SecondStepRegistrationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    def validate_phone_number(self, phone_number):
        pattern = r'^0\d{10}$'
        phone_number_exists: bool = User.objects.filter(phone_number=phone_number).exists()
        response = bool(re.match(pattern, str(phone_number)) and not phone_number_exists)
        if response:
            return True
        raise serializers.ValidationError("Invalid phone number format")