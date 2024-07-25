from typing import Optional, Type, Any

from django.contrib import admin
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest, HttpResponseRedirect


class LimitOneInstanceAdminMixin(admin.ModelAdmin):
    """
    A Django admin mixin that enforces a singleton model instance in the admin interface.
    It prevents the addition of new instances if one already exists, disables the deletion
    option, and redirects to the existing instance if trying to add a new one.

    Methods:
    - has_add_permission: Checks if adding a new instance is permissible.
    - has_delete_permission: Ensures that instances cannot be deleted.
    - change_view: Redirects to the existing instance's change page if it exists.
    """

    model: Type[Model]  # Annotate with the expected model type.

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Determine if the user has permission to add a new instance.
        If an instance already exists, return False.

        Args:
        - request: HttpRequest object containing metadata about the request.

        Returns:
        - bool: True if adding permission is granted, False otherwise.
        """
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(
        self, request: HttpRequest, obj: Optional[Model] = None
    ) -> bool:
        """
        Determine if the user has permission to delete the instance.
        Always returns False to prevent deletion.

        Args:
        - request: HttpRequest object containing metadata about the request.
        - obj: The model instance that is being considered for deletion.

        Returns:
        - bool: Always False to disable deletion.
        """
        return False

    def change_view(
        self,
        request: HttpRequest,
        object_id: str,
        form_url: str = "",
        extra_context: Optional[dict] = None,
    ) -> HttpResponseRedirect:
        """
        Overrides the default change view to redirect to the change page of the
        singleton instance if it exists and an addition is attempted.

        Args:
        - request: HttpRequest object containing metadata about the request.
        - object_id: The ID of the object to change.
        - form_url: URL for the form endpoint.
        - extra_context: Additional context to include in the response.

        Returns:
        - HttpResponseRedirect: Redirect to the existing instance change page or proceed as normal.
        """
        if not object_id and self.model.objects.exists():
            instance = self.model.objects.get()
            url = request.path + str(instance.id) + "/"
            return HttpResponseRedirect(url)
        return super().change_view(request, object_id, form_url, extra_context)


class ReadOnlyAdmin(admin.ModelAdmin):
    """
    A ModelAdmin class that restricts all modifications, making the admin interface read-only.

    This class overrides the add, change, and delete permissions to prevent any modifications
    to the model instances through the admin interface.
    """

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Disable the add permission in the admin interface."""
        return False

    def has_change_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        """Disable the change permission in the admin interface."""
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        """Disable the delete permission in the admin interface."""
        return False
