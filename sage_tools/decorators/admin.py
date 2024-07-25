"""
Decorators
"""
from functools import wraps

from django.conf import settings
from django.http import HttpRequest


class AdminBypassDecorator:
    """
    A decorator class designed to wrap around Django view functions or context processors.
    Its primary purpose is to prevent the execution of the wrapped function and return an
    empty context dictionary when the incoming request targets an admin page. This is
    particularly useful for avoiding unnecessary processing and ensuring sensitive
    information or functionality isn't inadvertently exposed to admin interfaces.
    """

    EMPTY_CONTEXT = {}

    def __init__(self, func):
        """
        Initializes the decorator with the function to be decorated.

        Parameters:
            func (callable): The function that this decorator will wrap. It should be
                a Django view function or context processor that takes an HttpRequest
                object as its first parameter.
        """
        wraps(func)(self)
        self.func = func

    @staticmethod
    def is_admin_request(request: HttpRequest) -> bool:
        """
        Determines if the incoming request is targeting the Django admin page.

        Parameters:
            request (HttpRequest): The incoming request object from Django.

        Returns:
            bool: True if the request is for an admin page, False otherwise. It checks
                this by comparing the request path to the admin URL name configured in
                the Django settings (settings.DJANGO_ADMINISTRATOR_URL_NAME).
        """
        return request.path.startswith(f"/{settings.DJANGO_ADMIN_URL_PREFIX}/")

    def __call__(self, request: HttpRequest, *args, **kwargs):
        """
        Executes the decorator logic and the wrapped function. If the incoming request
        is for an admin page, it bypasses the function call and returns an empty context.
        Otherwise, it calls the original function with the given arguments and keyword
        arguments.

        Returns:
            dict: The context dictionary from the wrapped function or EMPTY_CONTEXT if
                the request is for an admin page.
        """
        if self.is_admin_request(request):
            return self.EMPTY_CONTEXT
        return self.func(request, *args, **kwargs)
