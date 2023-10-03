from django.conf import settings as django_settings

TRACKMAN_ENABLED = getattr(django_settings, "TRACKMAN_ENABLED", True)

default_tracking_models = {
    "default": None,
}

TRACKMAN_MODELS = getattr(django_settings, "TRACKMAN_MODELS", default_tracking_models)

TRACKMAN_DATABASE_ALIAS = getattr(
    django_settings, "TRACKMAN_DATABASE_ALIAS", "tracking"
)

TRACKMAN_ADMIN_CLASS = getattr(
    django_settings,
    "TRACKMAN_ADMIN_CLASS",
    "trackman.tracking.AdminTrackingHandler",
)


ADMIN_ACTION_LABELS = {
    "change": "admin updated",
    "deletion": "admin deleted",
    "addition": "admin added",
}
