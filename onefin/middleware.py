from movie_collection.models import RequestCounter


class RequestCounterMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    # One-time configuration and initialization.

    def __call__(self, request):
        request_counter = RequestCounter.objects.all().first()
        if request_counter:
            request_counter.request_count = int(request_counter.request_count) + 1
            request_counter.save()
        else:
            RequestCounter.objects.create(request_count=1)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
