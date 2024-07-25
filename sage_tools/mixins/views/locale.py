from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation
from django.views import View

from sage_tools.utils.locale import MultilingualService


class SetLanguageMixinView(View):
    """
    A Django view for setting the user's language preference.

    `SetLanguageView` extends Django's base `View` class to provide a POST method
    that allows users to switch their language preference. It updates the language
    setting based on the user's request and redirects them to a specified URL, which
    can be language-prefixed.

    Methods
    -------
    post(request, *args, **kwargs)
        Handles POST requests to set the user's language preference and redirects to a given URL.

    See Also
    --------
    django.views.View : The base class from which this view inherits.
    django.utils.translation : Used for activating language settings.
    kernel.utils.locale.MultilingualService : Provides utility for adding language prefix to URLs.

    Examples
    --------
    This view can be used in a Django project by including it in the URL configuration.
    It responds to POST requests with `language` and `next` parameters to set the language
    and redirect to the next page, respectively.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to set the user's language preference.

        This method retrieves the language preference from the POST request, activates
        the chosen language, and redirects the user to a specified URL, optionally with
        a language prefix. If no language is specified in the request, it defaults to the
        application's default language.

        Parameters
        ----------
        request : HttpRequest
            The HttpRequest object containing details of the current request.
        *args : list
            Variable length argument list.
        **kwargs : dict
            Arbitrary keyword arguments.

        Returns
        -------
        HttpResponseRedirect
            Redirects to the specified URL, with the language setting updated.

        Notes
        -----
        The method checks for the `language` and `next` parameters in the POST data.
        It uses `MultilingualService` to add a language prefix to the redirection URL
        if a non-default language is selected.
        """

        language = request.POST.get("language", settings.LANGUAGE_CODE)
        next_page = request.POST.get("next", "/")

        if language and language in dict(settings.LANGUAGES):
            translation.activate(language)
            next_page = MultilingualService.get_language_prefix(next_page, language)
            response = HttpResponseRedirect(next_page)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
            return response
        else:
            return HttpResponseRedirect(next_page)
