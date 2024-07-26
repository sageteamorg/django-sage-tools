from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from sage_tools.validators.numeral import HalfPointIncrementValidator


class RatingMixin(models.Model):
    """
    An abstract base class model designed to add a rating functionality to any model that requires it.
    This mixin introduces a standardized way to capture user ratings for various objects within the
    application, ensuring consistency and reusability across different parts of the system.

    The rating system implemented by this mixin allows for granular feedback, supporting not only whole
    numbers but also half-point increments within a defined range from 1 to 5. This flexibility accommodates
    a wide range of rating scenarios, from product reviews to service evaluations, enhancing the application's
    ability to gather and reflect nuanced user feedback.

    As an abstract model, RatingMixin does not create a database table on its own but serves as a building
    block for other models, allowing them to easily integrate a uniform rating system without the need for
    redundant code.
    """

    rating = models.FloatField(
        verbose_name=_("Rating"),
        default=1,
        help_text=_("Rate from 1 (lowest) to 5 (highest)."),
        validators=[
            MinValueValidator(1, message=_("Rating must be at least 1.")),
            MaxValueValidator(5, message=_("Rating cannot be more than 5.")),
            HalfPointIncrementValidator(
                message=_("Rating must be between 1 and 5 in half-point increments.")
            ),
        ],
        db_comment="User's rating from 1 to 5.",
    )

    class Meta:
        abstract = True
