from django.http import HttpResponseForbidden
from rest_framework.authtoken.models import Token
from user.models import User


class AuthorizationMiddleWare:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Unauthorized")

        response = self.get_response(request)
        return response


allowed_paths = ['/register/verify-token/',
                 '/register/verify-otp/',
                 '/register/state/']


class TokenCheck:
    allowed_paths = ['/register/verify-token/',
                     '/register/verify-otp/',
                     '/register/state/',
                     ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in TokenCheck.allowed_paths:
            token = request.headers.get('Authorization').split(' ')[1]
            user_information = Token.objects.get(key=token).user.id
            user = User.objects.filter(id=user_information).first()
            request.auth = user

        response = self.get_response(request)
        response['auth'] = user
        response.auth2 = user

        return response

