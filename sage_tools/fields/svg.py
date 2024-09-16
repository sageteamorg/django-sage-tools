import os

from django.contrib.admin.widgets import AdminFileWidget
from django.core.validators import FileExtensionValidator
from django.db import models

from sage_tools.widgets import SVGWidget


class SVGField(models.FileField):
    """Custom field for handling SVG files."""

    def __init__(self, *args, **kwargs):
        # Add the SVG file extension validator by default
        svg_validator = FileExtensionValidator(allowed_extensions=["svg"])
        validators = kwargs.pop("validators", [])
        validators.append(svg_validator)
        self.url = None
        super().__init__(*args, validators=validators, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if "validators" in kwargs:
            validators = kwargs["validators"]
            if validators and isinstance(validators[-1], FileExtensionValidator):
                validators = validators[:-1]
            kwargs["validators"] = validators
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value and os.path.exists(value):
            self.url = value
            with open(value, "r") as svg_file:
                return svg_file.read()
        return ""

    def to_python(self, value):
        """Ensure the value is converted to the SVG content."""
        if isinstance(value, str) and os.path.exists(value):
            return value
        return value

    def formfield(self, **kwargs):
        """Override formfield to manipulate the value and ensure it behaves like a FileField."""
        kwargs["widget"] = SVGWidget(url=self.url)
        return super().formfield(**kwargs)

    def value_to_string(self, obj):
        """Ensure serialization returns the file path."""
        value = self.value_from_object(obj)
        if value:
            return self.url
        return ""
