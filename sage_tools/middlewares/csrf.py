"""
This module provides a custom CSRF middleware that extends
Django's default CsrfViewMiddleware.
It allows for the use of a custom name for the CSRF token,
enhancing the flexibility of CSRF protection in Django applications.
The primary class provided is SecureCsrfMiddleware, which can be
used as a drop-in replacement for Django's default CSRF middleware.
"""

from django.http import FileResponse
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware as DjangoCsrfViewMiddleware
from django.utils.safestring import mark_safe


class SecureCsrfMiddleware(DjangoCsrfViewMiddleware):
    """
    SecureCsrfMiddleware extends the default CsrfViewMiddleware from
    Django to allow for a custom CSRF token name.
    It overrides the process_request and process_response methods
    to replace the standard 'csrfmiddlewaretoken'
    with a custom name defined in the class attribute 'secure_csrf_name'.
    This class provides a way to customize the CSRF token name for security
    or organizational preferences without altering the fundamental CSRF
    protection mechanisms.
    """

    # Define 'secure_csrf_name' as a class attribute
    secure_csrf_name = settings.CSRF_INPUT_NAME

    def process_request(self, request):
        """
        Processes incoming requests to replace the standard CSRF token
        name with the custom one.
        It checks for the presence of the custom CSRF token name in the
        POST data and, if found, replaces the default 'csrfmiddlewaretoken'
        with the custom token. This method ensures that the system recognizes
        the token under its new name during the request lifecycle.

        :param request: HttpRequest object representing the current request
        :return: The result of the parent class's process_request method
        """
        request.POST = request.POST.copy()
        if self.secure_csrf_name in request.POST:
            request.POST["csrfmiddlewaretoken"] = request.POST.pop(
                self.secure_csrf_name
            )[0]
        return super().process_request(request)

    def process_response(self, request, response):
        """
        Processes outgoing responses to replace occurrences of the default
        CSRF token name in the HTML content with the custom CSRF token name.
        It ensures that forms rendered in the response HTML use the custom
        token name, maintaining consistency with the request processing and
        providing a seamless experience.

        :param request: HttpRequest object representing the current request
        :param response: HttpResponse object representing the current response
        :return: The result of the parent class's process_response method with
        modified content
        """
        # Check if the response is a FileResponse instance
        if isinstance(response, FileResponse):
            # If it's a FileResponse, return it unmodified
            return response

        # If it's not a FileResponse, proceed with your original processing
        if hasattr(response, "content"):
            response.content = response.content.replace(
                b'name="csrfmiddlewaretoken"',
                mark_safe(f'name="{self.secure_csrf_name}"').encode(),
            )
        return super().process_response(request, response)
