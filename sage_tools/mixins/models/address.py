from django.db import models
from django.utils.translation import gettext_lazy as _


class AddressMixin(models.Model):
    """
    Base model for addresses, containing common fields used in all address types.
    """

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        help_text=_("A descriptive title for the address, such as 'Home' or 'Office'."),
        db_comment="Descriptive title for the address.",
    )
    country = models.CharField(
        verbose_name=_("Country"),
        max_length=100,
        help_text=_("The country where the address is located."),
        db_comment="Country of the address.",
    )
    province = models.CharField(
        verbose_name=_("Province"),
        max_length=100,
        help_text=_("The province, state, or regional division of the address."),
        db_comment="Province or state of the address.",
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=100,
        help_text=_("The city or town of the address."),
        db_comment="City or town of the address.",
    )
    postal_address = models.TextField(
        verbose_name=_("Postal Address"),
        help_text=_(
            "The full postal address, including street name, number, and any additional details."
        ),
        db_comment="Full detailed postal address.",
    )
    postal_code = models.CharField(
        verbose_name=_("Postal Code"),
        max_length=20,
        help_text=_("The postal or ZIP code for the address."),
        db_comment="Postal or ZIP code of the address.",
    )
    plaque = models.CharField(
        verbose_name=_("Plaque"),
        max_length=20,
        help_text=_("The specific plaque number of the building or house."),
        db_comment="Plaque number of the building or house.",
    )
    building_unit = models.CharField(
        verbose_name=_("Building Unit"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("The unit or apartment number within a building, if applicable."),
        db_comment="Unit or apartment number in a building, optional.",
    )

    class Meta:
        abstract = True
