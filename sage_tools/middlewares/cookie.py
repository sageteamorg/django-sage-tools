"""
This module provides middleware support for handling user language
preferences in a Django web application. 
It extends Django's built-in locale middleware functionality,
offering a more nuanced approach to 
language detection and selection through URL prefixes and cookies.
The core component, CookieLocaleMiddleware, 
intercepts web requests to determine the most suitable language
for the user and adjust the request or response accordingly.
"""

import logging

from django.conf import settings
from django.middleware.locale import LocaleMiddleware as DjangoLocaleMiddleware
from django.shortcuts import redirect
from django.utils import translation

from sage_tools.utils.locale import MultilingualService

logger = logging.getLogger(__name__)


class CookieLocaleMiddleware(DjangoLocaleMiddleware):
    """
    Extends Django's LocaleMiddleware to manage language settings more dynamically.

    The middleware determines the user's preferred language by examining the URL and cookies,
    then aligns the request with the determined preference. It's designed to work seamlessly
    with multilingual sites, redirecting users to the appropriate language version of the site
    based on their preferences and the available languages.
    """

    def process_request(self, request):
        """
        Examines and aligns the request with the user's preferred language based
        on the URL or cookies.

        This method checks the request path for language prefixes (e.g., '/en/', '/fr/')
        and compares it with the language specified in the user's language cookie.
        It activates the appropriate language for the session and redirects to a URL
        that matches the preferred language if necessary.

        Example:
            When a user accesses a URL like '/es/about/', but their language cookie
            is set to 'en', this method will redirect them to '/en/about/' if
            English is an available language. Conversely, if the URL is '/about/' with no
            language prefix and the cookie is set to 'es', the user will be redirected to '/es/about/'.

        Parameters:
            request: HttpRequest object containing metadata about the request.

        Returns:
            A redirect response if the language from the URL and cookie differ, otherwise None.
        """

        # Exclude certain paths from language prefix redirection
        if request.path_info.startswith(
            "/set-language/"
        ) or request.path_info.startswith("/i18n/"):
            return super().process_request(request)

        # Retrieve the language from the URL and the cookie
        url_language = translation.get_language_from_path(request.path_info)
        cookie_language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)

        # Ensure that the URL is clean of language prefixes for accurate redirection
        clean_path = MultilingualService.remove_language_prefix(request.path_info)

        # Check if the cookie language is valid
        if cookie_language in dict(settings.LANGUAGES):
            # Activate the cookie language and set it in the request
            translation.activate(cookie_language)
            request.LANGUAGE_CODE = cookie_language

            # Redirect to the correct language URL, considering the default language case
            if cookie_language != settings.LANGUAGE_CODE and (
                not url_language or url_language != cookie_language
            ):
                new_path = MultilingualService.add_language_prefix(
                    clean_path, cookie_language
                )
                return redirect(new_path)
            elif (
                cookie_language == settings.LANGUAGE_CODE
                and url_language
                and url_language != settings.LANGUAGE_CODE
            ):
                # Redirect to the clean path if the default language is set in the cookie and
                #  URL has a non-default prefix
                return redirect(clean_path)

        # If the URL language is valid, activate it
        elif url_language in dict(settings.LANGUAGES):
            translation.activate(url_language)
            request.LANGUAGE_CODE = url_language
            # Redirect if the URL language is different from the cookie language and is not
            #  the default language
            if (
                url_language != settings.LANGUAGE_CODE
                and url_language != cookie_language
            ):
                new_path = MultilingualService.add_language_prefix(
                    clean_path, url_language
                )
                return redirect(new_path)

        # Handle default language without prefix
        elif not url_language or url_language == settings.LANGUAGE_CODE:
            translation.activate(settings.LANGUAGE_CODE)
            request.LANGUAGE_CODE = settings.LANGUAGE_CODE
            # Redirect only if there was a language prefix and the cookie language is not
            #  the default language
            if url_language and cookie_language != settings.LANGUAGE_CODE:
                return redirect(clean_path)

        # Fallback to default language handling
        super().process_request(request)

    def process_response(self, request, response):
        """
        Modifies the response to set the correct language cookie based on
        the user's preferred language.

        After the parent class's process_response method runs, this method
        checks if the current language in the session differs from the one
        in the user's language cookie. If there is a difference, it updates
        the language cookie to the current session language.

        Example:
            If a user's session language is 'fr' (French) after interacting
            with the site, but their language cookie is still 'en' (English),
            this method will set the cookie to 'fr' in the response.
            The next time the user makes a request, their preferred
            language will be French.

        Parameters:
            request: HttpRequest object containing metadata about the request.
            response: HttpResponse object that will be sent back to the user.

        Returns:
            The modified HttpResponse object with the updated language cookie if necessary.
        """

        # First, call the parent class's process_response method
        response = super().process_response(request, response)

        # Get the current language
        current_language = translation.get_language()

        # Set the language cookie if it's different from the current one
        if (
            current_language
            and request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME) != current_language
        ):
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, current_language)

        return response
