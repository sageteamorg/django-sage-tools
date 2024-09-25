from django.core.exceptions import ValidationError

from sage_tools.utils.converters import UnitConvertor


class FileSizeValidator:
    def __init__(self, max_size):
        """
        Initialize the validator with the maximum file size.

        Args:
        max_size (int): Maximum file size in bytes.
        """
        self.max_size = max_size

    def __call__(self, value):
        """
        Check the file size and raise a ValidationError if it exceeds the limit.

        Args:
        value (File): The file being uploaded.
        """
        size = UnitConvertor.convert_byte_to_megabyte(self.max_size)
        if value.size > self.max_size:
            raise ValidationError(f"File size must not exceed {size} MB.")

    def deconstruct(self):
        """
        Deconstruct the validator for serialization.

        Returns:
            tuple: The full path of the object, positional arguments, and keyword arguments.
        """
        path = f"{self.__module__}.{self.__class__.__name__}"
        args = (self.max_size,)
        kwargs = {}
        return path, args, kwargs
