import logging
from typing import Any

from django.conf import settings
from django.http import HttpRequest
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from sage_tools.handlers.session import SessionHandler

logger = logging.getLogger(__name__)

try:
    import pytz
except ImportError:
    raise ImportError("Install `pytz` package. Run `pip install pytz`.")  # noqa: B904


class TimezoneMiddleware(MiddlewareMixin):
    """Middleware to handle setting the user's timezone based on their session
    data."""

    def process_request(self, request: HttpRequest) -> None:
        """Process the request to set the timezone from the session."""
        session_handler = SessionHandler(request)
        tzname = session_handler.get("user_timezone")
        if tzname:
            try:
                timezone.activate(pytz.timezone(tzname))
                # Set Django's timezone to the user's timezone
                settings.TIME_ZONE = tzname
            except pytz.UnknownTimeZoneError:
                logger.error(f"Unknown timezone: {tzname}")
                timezone.deactivate()
        else:
            timezone.deactivate()

    def process_response(self, request: HttpRequest, response) -> Any:
        """Ensure the timezone is deactivated after the response is
        processed."""
        timezone.deactivate()
        return response
