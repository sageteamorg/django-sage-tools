import os

from django.conf import settings
from django.db import models

try:
    from sorl.thumbnail import ImageField
except ImportError:
    raise ImportError(  # noqa: B904
        "Install `sorl-thumbnail` package. Run `pip install sorl-thumbnail`."
    )


class FileDeletionHandler:
    """A handler for managing file deletions linked to Django model fields.

    This class provides methods to identify file fields in a model, delete old
    files when new ones are uploaded, and orchestrate the overall file deletion
    process based on application settings and model instance states.

    Methods
    -------
    is_file_field(field):
        Determine if the given field is a file field.

    delete_old_file(old_instance, field_name):
        Delete the file from the specified field in the provided instance.

    handle_deletion(sender, instance):
        Conduct a check and delete operation for file fields of the given model instance.

    """

    @staticmethod
    def is_file_field(field):
        """Check if the provided field is a type of file field.

        Parameters
        ----------
        field : django.db.models.fields
            A Django model field to be checked against file field types.

        Returns
        -------
        bool
            True if the field is a FileField, ImageField, or a custom ImageField
            from `sorl.thumbnail`, otherwise False.

        """
        return (
            isinstance(field, models.FileField)  # noqa: PLR1701
            or isinstance(field, models.ImageField)
            or isinstance(field, ImageField)
        )

    @staticmethod
    def delete_old_file(old_instance, field_name):
        """Delete the file associated with the provided field name in the old
        instance if it exists.

        Parameters
        ----------
        old_instance : django.db.models.Model
            The old instance of the model before the update.
        field_name : str
            The name of the field which potentially holds a file to be deleted.

        Notes
        -----
        This method directly interacts with the file system to delete files and should
        be used with caution to avoid accidental data loss.

        """
        old_file = getattr(old_instance, field_name, None)
        if old_file and os.path.isfile(old_file.path):
            os.remove(old_file.path)

    @classmethod
    def handle_deletion(cls, sender, instance):
        """Handle the deletion of files for the provided instance based on the
        application settings and instance state.

        Parameters
        ----------
        sender : django.db.models.Model
            The model class sending the signal.
        instance : django.db.models.Model
            The instance of the model being saved, potentially containing file fields to check.

        Notes
        -----
        This method orchestrates the deletion process by iterating over all fields of
        the instance, checking for file changes, and deleting old files as necessary.
        It respects the `CLEANUP_DELETE_FILES` setting to determine if deletion should occur.

        """
        if not getattr(settings, "CLEANUP_DELETE_FILES", True):
            return  # If file deletion is disabled, do nothing

        if not instance.pk:
            return  # If the instance is new, there's no old file to delete

        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return  # Old instance doesn't exist

        for field in instance._meta.fields:
            if cls.is_file_field(field):
                old_file = getattr(old_instance, field.name, None)
                new_file = getattr(instance, field.name, None)
                if old_file != new_file:
                    cls.delete_old_file(old_instance, field.name)
