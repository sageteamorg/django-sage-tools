import pytest
from django.core.exceptions import ValidationError
from sage_tools.validators.string import NameValidator


class TestNameValidator:
    """Test suite for the `NameValidator` class."""

    def test_valid_values(self):
        """Test that `NameValidator` accepts valid name values."""
        validator = NameValidator()
        valid_names = [
            "John Doe",
            "Mary-Jane O'Connor",
            "Anne Marie",
            "O'Reilly",
            "Smith-Jones",
        ]

        for name in valid_names:
            validator(name)

    def test_invalid_values(self):
        """Test that `NameValidator` raises `ValidationError` for invalid name
        values."""
        validator = NameValidator()
        invalid_names = ["John123", "Mary@Jane", "Anne_Marie", "O'Reilly!", ""]

        for name in invalid_names:
            with pytest.raises(ValidationError):
                validator(name)

    def test_custom_message(self):
        """Test that `NameValidator` uses a custom error message."""
        custom_message = "Custom error message"
        validator = NameValidator(message=custom_message)

        with pytest.raises(ValidationError) as exc_info:
            validator("Invalid@Name")
        assert exc_info.value.message == custom_message
