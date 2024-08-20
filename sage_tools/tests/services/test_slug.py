from unittest.mock import patch
from django.utils.text import slugify
from sage_tools.services.slug import SlugService


class TestSlugService:
    """Test suite for the `SlugService` class."""

    @patch.object(SlugService, "_is_slug_unique")
    def test_generate_unique_slug(
        self, mock_is_slug_unique, slug_service, mock_instance
    ):
        mock_is_slug_unique.side_effect = [False, True]
        base_slug = "test-title"
        unique_slug = slug_service._generate_unique_slug(base_slug)
        assert unique_slug == "test-title-1"

    @patch.object(SlugService, "has_slug_changed", return_value=True)
    def test_has_slug_changed(self, mock_has_slug_changed, slug_service, mock_instance):
        assert slug_service.has_slug_changed("new-slug") is True

    @patch.object(SlugService, "_is_slug_unique", return_value=True)
    @patch.dict(
        "django.conf.settings._wrapped.__dict__", {"AUTO_SLUGIFY_ENABLED": True}
    )
    def test_create_unique_slug(self, mock_is_slug_unique, slug_service, mock_instance):
        unique_slug = slug_service.create_unique_slug()
        assert unique_slug == slugify("Test Title", allow_unicode=True)

    @patch.dict(
        "django.conf.settings._wrapped.__dict__", {"AUTO_SLUGIFY_ENABLED": True}
    )
    def test_create_slug_with_auto_slugify_enabled(self, slug_service, mock_instance):
        generated_slug = slug_service._create_slug()
        assert generated_slug == slugify("Test Title", allow_unicode=True)

    @patch.dict(
        "django.conf.settings._wrapped.__dict__", {"AUTO_SLUGIFY_ENABLED": False}
    )
    def test_create_slug_with_auto_slugify_disabled(self, slug_service, mock_instance):
        slug_service.auto_slugify_enabled = False
        generated_slug = slug_service._create_slug()
        assert generated_slug == mock_instance.slug
