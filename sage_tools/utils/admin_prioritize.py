from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import site


def get_app_list(self, request, app_label=None):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    app_dict = self._build_app_dict(request)

    # Filter by app_label if provided
    if app_label:
        app_dict = {app_label: app_dict[app_label]} if app_label in app_dict else {}

    if not app_dict:
        return

    for app_name in list(app_dict.keys()):
        app = app_dict[app_name]
        model_priority = {}
        for model in app["models"]:
            try:
                model_instance = apps.get_model(app_name, model["object_name"])
                model_priority[model["object_name"]] = getattr(
                    site._registry[model_instance],
                    "admin_priority",
                    20,
                )
            except LookupError:
                # This handles the case where a model cannot be found (e.g., for the 'constance' app)
                continue

        # Sort models in the app by their priority
        app["models"].sort(key=lambda x: model_priority.get(x["object_name"], 20))

    # Sort the apps by their name
    app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())
    return app_list


admin.AdminSite.get_app_list = get_app_list
