from django.http import HttpResponseForbidden
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from user.models import User


class AuthorizationMiddleWare:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Unauthorized")

        response = self.get_response(request)
        return response


class TokenCheck:
    allowed_paths = ['/register/verify-token/',
                     '/register/verify-otp/',
                     '/register/state/',
                     ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in TokenCheck.allowed_paths:
            authorization_header = request.META.get('HTTP_AUTHORIZATION').split(' ')[-1]
            try:
                user_information = Token.objects.get(key=authorization_header).user.id
                user = User.objects.filter(id=user_information).first()
                request.META['HTTP_AUTHORIZATION'] = authorization_header
                request.META['user'] = user
            except :
                response = self.get_response(request)
                return response

        response = self.get_response(request)

        return response
