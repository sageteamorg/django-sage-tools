"""
This module provides a Django model class for image manipulation and retrieval.
It includes methods for converting image formats, cropping images, and generating
thumbnails.
"""

import io
import os
from pathlib import Path

from django.core.files import File
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

try:
    from PIL import Image
except ImportError:
    raise ImportError(
        "The `Pillow` package is required but not installed. "
        "Please install it by running: pip install pillow"
    )

try:
    from sorl.thumbnail import get_thumbnail
except ImportError:
    raise ImportError(
        "The `sorl-thumbnail` package is required but not installed. "
        "Please install it by running: pip install sorl-thumbnail"
    )


class PictureOperationAbstract(models.Model):
    """
    An abstract Django model class for performing various operations on images.
    This class provides functionalities for image conversion, cropping, thumbnail
    generation, and retrieving image properties like URL, size, and dimensions.
    """

    picture: str

    alternate_text = models.CharField(
        verbose_name=_("Picture Alternate Text"),
        max_length=110,
        validators=[MaxLengthValidator(150), MinLengthValidator(3)],
        null=True,
        blank=True,
        help_text=_("Write about picture for SEO"),
        db_comment=_("Alternative text for the picture, used for SEO purposes."),
    )

    width_field = models.PositiveSmallIntegerField(
        verbose_name=_("Picture Width"),
        null=True,
        blank=True,
        editable=False,
        help_text=_("size of picture's Width"),
        db_comment=_("The width of the picture in pixels."),
    )

    height_field = models.PositiveSmallIntegerField(
        verbose_name=_("Picture Height"),
        null=True,
        blank=True,
        editable=False,
        help_text=_("size of picture's Height"),
        db_comment=_("The height of the picture in pixels."),
    )

    class Meta:
        """
        Meta
        """

        abstract = True

    def convert_to_webp(self):
        """
        Converts the image associated with this model instance to the WEBP format.
        The converted image replaces the original image.
        """
        if ".webp" not in self.picture.path:
            path = self.picture.path
            # format_ = Path(path).suffix
            with Image.open(path) as data:
                data_rgb = data.convert("RGB")
                output = io.BytesIO()
                data_rgb.save(output, format="webp")
                self.picture.save(
                    os.path.basename(path).replace(format, ".webp"), output
                )

    def convert_to_jpg(self):
        """
        Converts the image associated with this model instance to JPEG format.
        The converted image replaces the original image.
        """
        if ".jpg" not in self.picture.path:
            path = self.picture.path
            format = Path(path).suffix

            with Image.open(path) as data:
                data_rgb = data.convert("RGB")
                output = io.BytesIO()
                data_rgb.save(output, format="JPEG")
                self.picture.save(
                    os.path.basename(path).replace(format, ".jpg"), output
                )

    def convert_to_png(self):
        """
        Converts the image associated with this model instance to PNG format.
        The converted image replaces the original image and the original file is removed.
        """
        if ".png" not in self.picture.path:
            path = self.picture.path
            format = Path(path).suffix

            with File(open(self.picture.path, "rb")) as data:
                self.picture.save(
                    os.path.basename(self.picture.path).replace(format, ".png"), data
                )
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    def crop(self, left, top, right, bottom):
        """
        Crops the image associated with this model instance.

        Parameters:
            left (int): The left boundary of the crop box.
            top (int): The upper boundary of the crop box.
            right (int): The right boundary of the crop box.
            bottom (int): The lower boundary of the crop box.
        """
        path = self.picture.path
        with Image.open(path) as pic:
            pic_rgb = pic.convert("RGB")
            data = pic_rgb.crop((left, top, right, bottom))
            output = io.BytesIO()
            data.save(output, format="JPEG")
            self.picture.save(os.path.basename(path), output)

    def get_thumbnail(self, size="100x100"):
        """
        Generates a thumbnail for the image associated with this model instance.
        """
        return get_thumbnail(self.picture, crop="center", quality=99)

    def get_thumbnail_url(self, size="100x100"):
        """
        Retrieves the URL of the thumbnail for the image associated with this model instance.
        """
        return get_thumbnail(self.picture, crop="center", quality=99).url

    def get_picture_url(self):
        """
        Retrieves the URL of the image associated with this model instance.
        """
        return self.picture.url

    def get_picture_size(self):
        """
        Retrieves the file size of the image associated with this model instance.
        """
        return self.picture.size

    def get_picture_dimensions(self):
        """
        Retrieves the dimensions of the image associated with this model instance.
        """
        return (self.picture.width, self.picture.height)

    def get_file_name(self):
        """
        Retrieves the file name of the image associated with this model instance.
        """
        return os.path.basename(self.picture.name)
