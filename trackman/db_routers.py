from django.apps import apps

from trackman import settings as trackman_settings
from trackman.models import TrackingBaseModel


class TrackingDatabaseRouter:
    """
    A Database Router that allows tracking models to be defined in a separate database.
    The tracking database is identified by a database alias, as defined by Django `DATABASES`
    setting.

    Tracking models are discovered automatically at runtime.
    """

    def __init__(self):
        """
        Initialize the router by setting the database alias from settings,
        and building the list of the app labels and tracking models.
        """
        self.database_alias = trackman_settings.TRACKMAN_DATABASE_ALIAS
        self.tracking_app_labels = self.get_tracking_app_labels()

    def get_tracking_app_labels(self):
        """
        Build and return a set of all unique app labels from installed apps
        where the models subclass `TrackingBaseModel`.
        """
        tracking_app_labels = set()
        for model in apps.get_models():
            if issubclass(model, TrackingBaseModel):
                tracking_app_labels.add(model._meta.app_label)
        return tracking_app_labels

    def is_in_tracking_app(self, model):
        """
        Checks if the given object lives in one of the tracking apps.
        """
        return model._meta.app_label in self.tracking_app_labels

    def db_for_read(self, model, **hints):
        """
        For READ operations, returns the tracking database alias if model's app label
        is part of the tracking apps.
        """
        if self.is_in_tracking_app(model):
            return self.database_alias
        return None

    def db_for_write(self, model, **hints):
        """
        For WRITE operations, returns the tracking database alias if model's app label
        is part of the tracking apps.
        """
        if self.is_in_tracking_app(model):
            return self.database_alias
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations only if both objects are defined in tracking apps.
        """
        if self.is_in_tracking_app(obj1) and self.is_in_tracking_app(obj2):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Determines if migration is allowed to a particular database.
        """
        if app_label in self.tracking_app_labels:
            return db == self.database_alias
        return None
