import importlib

from django.apps import apps

from trackman import settings as trackman_settings


def get_tracking_model(model_alias):
    """
    Return the model class instructed in the `TRACKMAN_MODELS` settings,
    where `model_alias` represents the key of the settings dictionary.
    """
    model_dot_string = trackman_settings.TRACKMAN_MODELS[model_alias]
    app_label, model_name = model_dot_string.rsplit(".", 1)
    model_class = apps.get_model(app_label=app_label, model_name=model_name)
    return model_class


def get_admin_tracking_class():
    """
    Return the class module looking at settings.
    """
    class_dot_string = trackman_settings.TRACKMAN_ADMIN_CLASS
    module_name, class_name = class_dot_string.rsplit(".", 1)
    tracking_module = importlib.import_module(module_name)
    tracking_class = getattr(tracking_module, class_name)
    return tracking_class
