"""A module for handling multilingual URL prefixes in Django applications.

This module provides the `MultilingualService` class, which offers methods
to add or remove language prefixes in URLs based on the application's language
settings. It's designed to assist in creating and managing URLs in a multilingual
Django web application.

Classes
-------
MultilingualService

See Also
--------
django.conf.settings : Django's settings module where language settings are defined.

Notes
-----
The module is particularly useful in scenarios where a Django application serves
content in multiple languages and needs to modify URLs to reflect the current
language context.

"""

from django.conf import settings


class MultilingualService:
    """A service class for managing language prefixes in URLs.

    This class provides class methods to add or remove language prefixes from URLs,
    assisting in the creation of language-specific URLs in a multilingual Django application.
    It uses the application's language settings defined in Django's settings module.

    Methods
    -------
    get_language_prefix(url, language)
        Processes the given URL and adds or removes the language prefix based on the
        specified language.
    add_language_prefix(url, language)
        Adds the specified language prefix to the given URL.
    remove_language_prefix(url)
        Removes any existing language prefix from the given URL.

    Examples
    --------
    >>> MultilingualService.get_language_prefix('/example/', 'fr')
    '/fr/example/'
    >>> MultilingualService.add_language_prefix('/example/', 'es')
    '/es/example/'
    >>> MultilingualService.remove_language_prefix('/de/example/')
    '/example/'

    """

    @classmethod
    def get_language_prefix(cls, url, language):
        """Process the given URL to add or remove the language prefix based on
        the specified language.

        This method first removes any existing language prefix from the URL and then,
        if the specified language is not the default language, adds the appropriate language prefix.

        Parameters
        ----------
        url : str
            The URL to process.
        language : str
            The language code to apply to the URL.

        Returns
        -------
        str
            The URL with the appropriate language prefix added, if necessary.

        """
        url = cls.remove_language_prefix(url)
        if language != settings.LANGUAGE_CODE:
            return cls.add_language_prefix(url, language)
        return url

    @classmethod
    def add_language_prefix(cls, url, language):
        """Add the specified language prefix to the given URL.

        This method formats the URL by prefixing it with the specified language code.

        Parameters
        ----------
        url : str
            The URL to which the language prefix will be added.
        language : str
            The language code to use as a prefix.

        Returns
        -------
        str
            The URL prefixed with the specified language code.

        """
        return f"/{language}{url}"

    @classmethod
    def remove_language_prefix(cls, url):
        """Remove any existing language prefix from the given URL.

        This method iterates through the available languages and removes the corresponding prefix
        from the URL, if present. It is designed to strip language codes from URLs in a
        language-agnostic manner.

        Parameters
        ----------
        url : str
            The URL from which the language prefix will be removed.

        Returns
        -------
        str
            The URL with any language prefix removed.

        """
        for lang_code, _ in settings.LANGUAGES:
            prefix = f"/{lang_code}/"
            if url.startswith(prefix):
                return url[len(prefix) - 1 :]
        return url
