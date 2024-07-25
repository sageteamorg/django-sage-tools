from django.conf import settings
from django.http import HttpRequest


def get_maintenance_variables(request: HttpRequest):
    context = dict()
    context["is_maintenance_enabled"] = getattr(settings, "UNDER_CONSTRUCTION_MODE")
    context["is_coming_soon_enabled"] = getattr(settings, "COMING_SOON_MODE")
    return context
