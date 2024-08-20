import pytest
from django.core.exceptions import ValidationError
from sage_tools.validators.numeral import HalfPointIncrementValidator


class TestHalfPointIncrementValidator:
    """Test suite for the `HalfPointIncrementValidator` class."""

    def test_valid_values(self):
        """Test that `HalfPointIncrementValidator` accepts valid values."""
        validator = HalfPointIncrementValidator()
        valid_values = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

        for value in valid_values:
            validator(value)

    def test_invalid_values(self):
        """Test that `HalfPointIncrementValidator` raises `ValidationError` for
        invalid values."""
        validator = HalfPointIncrementValidator()
        invalid_values = [0.5, 5.5, 3.2, 6, 0]

        for value in invalid_values:
            with pytest.raises(ValidationError):
                validator(value)

    def test_custom_message(self):
        """Test that `HalfPointIncrementValidator` uses a custom error
        message."""
        custom_message = "Custom error message"
        validator = HalfPointIncrementValidator(message=custom_message)

        with pytest.raises(ValidationError) as exc_info:
            validator(3.3)
        assert exc_info.value.message == custom_message
