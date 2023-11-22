import re
from rest_framework import serializers


class ThirdStepRegistrationSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required=True)
    cars = serializers.IntegerField(required=True)
    company_name = serializers.CharField(required=True)

    def validate_company_name(self, company_name):
        pattern = r'^[\u0600-\u06FF\s]+$'
        response = re.match(pattern, company_name) is not None
        return response
