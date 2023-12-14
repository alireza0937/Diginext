import re
from rest_framework import serializers


class FirstStepRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_password(self, password):
        password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{6,}$'
        if bool(re.match(password_pattern, password)):
            return password
        raise serializers.ValidationError

    def validate_username(self, username):
        username_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\s]*$'
        if bool(re.match(username_pattern, username)):
            return username
        raise serializers.ValidationError
