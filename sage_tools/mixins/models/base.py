import uuid

from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _

from sage_tools.services.slug import SlugService


class TimeStampMixin(models.Model):
    """
    A mixin class that adds self-updating `created_at` and `modified_at` fields to a
    Django model.

    This mixin automatically records the creation time of an object and updates the
    modification time
    every time the object is saved. It is an abstract base class, meaning it does not
    correspond to a database table. Instead, its fields are added to each model that
    inherits from it.

    ```
    class MyModel(TimeStampMixin, models.Model):
        # other fields here
    ```

    This will add `created_at` and `modified_at` fields to `MyModel`.

    The class is marked as abstract in Django, which means it will not be used to create
    any database table. Instead, its fields are added to those of the child class.

    """

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified at"), auto_now=True)

    class Meta:
        """
        Meta
        """

        abstract = True


class StockUnitMixin(models.Model):
    """
    Abstract Django Model that contains:
        sku
    """

    sku = models.UUIDField(
        _("Stock of Unit"),
        max_length=100,
        default=uuid.uuid4,
        unique=True,
        help_text=_(
            "A unique identifier assigned to each product in inventory. "
            "This Stock Unit SKU is used to uniquely identify and manage"
            " products in your inventory."
        ),
    )

    class Meta:
        abstract = True


class BaseTitleSlugMixin(models.Model):
    """
    A mixin class that adds a title and slug field to a model.

    The `TitleSlugMixin` provides a standardized way to include title and slug fields in
    various models. It includes a `title` field, which is a CharField with a maximum
    length of 255 characters and is unique across the model it's used in. The `slug`
    field is a SlugField used for URL-friendly representations of the `title`, also
    unique and limited to 255 characters.
    """

    title = models.CharField(
        _("Title"),
        max_length=255,
        unique=True,
        help_text=_("Enter a unique title."),
        db_comment="Stores the unique title of the instance.",
    )

    slug = models.SlugField(
        _("Slug"),
        max_length=255,
        unique=True,
        editable=True,
        allow_unicode=True,
        help_text=_("URL-friendly slug from the title."),
        db_comment="Stores the URL-friendly slug derived from the title.",
    )

    @admin.display(description=_("title"), ordering=("-title"))
    def get_title(self) -> str:
        """
        Returns the title of the instance, shortened to 30 characters if necessary.

        This method is used to display a shortened version of the title in the Django
        admin interface if the title is longer than 30 characters. It appends ellipses
        to indicate that the title has been truncated.

        Returns:
            str: The full title if it's less than 30 characters, otherwise the first 30
            characters followed by '...'.
        """
        TRUNCATE_SIZE = 30
        return (
            self.title if len(self.title) < TRUNCATE_SIZE else (self.title[:30] + "...")
        )

    class Meta:
        """The Meta class of the TitleSlugMixin has an attribute abstract = True,
        making it an abstract class and the fields defined in it will be used in the
        child classes. The Meta class does not have any other attributes.
        """

        abstract = True

    def __str__(self) -> str:
        """
        String representation of the instance.

        Returns the title of the instance, providing a readable representation of the
        instance in admin panels or debug outputs.
        """
        return self.title


class TitleSlugMixin(BaseTitleSlugMixin):
    """
    A mixin class that adds a title and slug field to a model.

    The `TitleSlugMixin` provides a standardized way to include title and slug fields in
    various models. It includes a `title` field, which is a CharField with a maximum
    length of 255 characters and is unique across the model it's used in. The `slug`
    field is a SlugField used for URL-friendly representations of the `title`, also
    unique and limited to 255 characters.
    """

    def save(self, *args, **kwargs):
        slug_service = SlugService(self)
        self.slug = slug_service.create_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        """The Meta class of the TitleSlugMixin has an attribute abstract = True,
        making it an abstract class and the fields defined in it will be used in the
        child classes. The Meta class does not have any other attributes.
        """

        abstract = True

    def __str__(self) -> str:
        """
        String representation of the instance.

        Returns the title of the instance, providing a readable representation of the
        instance in admin panels or debug outputs.
        """
        return self.title



class BaseTitleSlugDescriptionMixin(BaseTitleSlugMixin):
    """
    A mixin class that extends TitleSlugMixin by adding a description field.

    This mixin inherits from TitleSlugMixin and adds a `description` field. It's
    designed to be used in models where an additional descriptive text field is
    necessary along with the title and slug. The `description` field is a TextField,
    suitable for longer text.
    """

    description = models.TextField(
        _("Description"),
        help_text=_(
            "Enter a detailed description of the item. This can include its purpose, "
            "characteristics, and any other relevant information."
        ),
        db_comment="Stores a detailed description of the instance.",
    )

    class Meta:
        """
        Meta class for TitleSlugDescriptionMixin.
        """

        abstract = True


class TitleSlugDescriptionMixin(TitleSlugMixin):
    """
    A mixin class that extends TitleSlugMixin by adding a description field.

    This mixin inherits from TitleSlugMixin and adds a `description` field. It's
    designed to be used in models where an additional descriptive text field is
    necessary along with the title and slug. The `description` field is a TextField,
    suitable for longer text.
    """

    description = models.TextField(
        _("Description"),
        help_text=_(
            "Enter a detailed description of the item. This can include its purpose, "
            "characteristics, and any other relevant information."
        ),
        db_comment="Stores a detailed description of the instance.",
    )

    class Meta:
        """
        Meta class for TitleSlugDescriptionMixin.
        """

        abstract = True
