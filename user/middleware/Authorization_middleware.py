from django.http import HttpResponseForbidden, HttpRequest


class AuthorizationMiddleWare:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Unauthorized")

        response = self.get_response(request)
        return response
