from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class HalfPointIncrementValidator:
    message = _("Ensure your rating is in half-point increments within the range of 1 to 5.")
    code = 'invalid_half_point_increment'
    
    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
    
    def __call__(self, value):
        if not (1 <= value <= 5) or ((value * 2) % 1 != 0):
            raise ValidationError(self.message, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.message == other.message and
            self.code == other.code
        )
