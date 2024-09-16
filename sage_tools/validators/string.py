import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class NameValidator:
    message = _(
        "Enter a valid name. The name can only contain letters, spaces, hyphens, and apostrophes. Examples: John Doe, Mary-Jane O'Connor."
    )
    code = "invalid_name"
    regex = r"^[a-zA-Z]+([ '\-][a-zA-Z]+)*$"

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if not re.match(self.regex, value):
            raise ValidationError(self.message, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.message == other.message
            and self.code == other.code
            and self.regex == other.regex
        )
