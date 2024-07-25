from typing import Any

from django.conf import settings
from django.utils.text import slugify


class SlugService:
    """
    A service class for handling slug creation and uniqueness for a given model instance.

    The `SlugService` class provides methods to create slugs from the instance title,
    check if a slug has been modified, and ensure the uniqueness of slugs within the model.
    It uses the `AUTO_SLUGIFY_ENABLED` setting to determine whether to automatically generate
    slugs from the instance title.
    """

    def __init__(self, instance: Any) -> None:
        self.instance = instance
        self.auto_slugify_enabled: bool = getattr(
            settings, "AUTO_SLUGIFY_ENABLED", True
        )

    def _create_slug(self) -> str:
        """Generate a slug from the instance title if auto-slugify is enabled, otherwise use the existing slug."""
        if self.auto_slugify_enabled:
            return slugify(self.instance.title, allow_unicode=True)
        return self.instance.slug

    def _is_slug_unique(self, slug: str) -> bool:
        """Check if a given slug is unique among the instances."""
        return (
            not type(self.instance)
            .objects.filter(slug=slug)
            .exclude(pk=self.instance.pk)
            .exists()
        )

    def _generate_unique_slug(self, base_slug: str) -> str:
        """Generate a unique slug by appending a counter if needed."""
        new_slug = base_slug
        counter = 1
        while not self._is_slug_unique(new_slug):
            new_slug = f"{base_slug}-{counter}"
            counter += 1
        return new_slug

    def has_slug_changed(self, new_slug: str) -> bool:
        """Check if the slug has been modified compared to the stored slug."""
        if not self.instance.pk:
            return False
        existing_instance = type(self.instance).objects.get(pk=self.instance.pk)
        return existing_instance.slug != new_slug

    def create_unique_slug(self) -> str:
        """Create and return a unique slug for the instance."""
        base_slug = self._create_slug()
        return self._generate_unique_slug(base_slug)
