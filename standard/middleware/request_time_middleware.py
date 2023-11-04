import datetime


class RequestTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.start_time = datetime.datetime.now()
        response = self.get_response(request)
        return response
