Django Trackman
===============


Django Trackman helps with tracking and logging.


Features
--------

- Customizable tracking models: Django-trackman provides the base models and an admin class mixin
  that you can extend to define your own tracking models.

- Loose coupling: The tracking table is not related to you application table with foreign keys.
  This ensures that your tracking data is kept independent of your application data.

- Separate tracking database: You can decide to use a separate database for your tracking data that could grow fast.
  A database router will help you implement the Django multiple database feature.

- Admin action tracking: Django-trackman lets you enable tracking of Django admin actions.


Installation
------------

.. code-block:: shell

    pip install django-trackman


Add 'trackman' to your INSTALLED_APPS in Django's settings:


.. code-block:: python

    INSTALLED_APPS = (
        ...
        'trackman',
        ...
    )


Then enable trackman by setting the variable `TRACKMAN_ENABLED` to `True`.


Tracking Models
---------------

Django Trackman can be used to create custom tracking models.
Here's an example of a model class that extends Django Trackman's TrackingBaseModel:


.. code-block:: python

    from trackman.models import TrackingBaseModel
    from django.db import models

    class TrackingAction(TrackingBaseModel):
        team = models.CharField("Team", max_length=256, blank=True)

        def __str__(self):
            return f"Actor: {self.actor}, Action: {self.action}, Time: {self.created}"

        class Meta:
            verbose_name = "Action Log"
            verbose_name_plural = "Action Logs"



How Django Trackman would know that this model should be used by default for tracking
your actions ? You'll need to instruct it by defining a default tracking model in
your settings.

.. code-block:: python

  TRACKMAN_MODELS = {
      "default": "tracking.TrackingAction",
      "data-quality": "tracking.DataQualityTracking",
  }

Here, you'll notice that we have also defined a additional tracking model for data
quality tracking.


Admin
-----

For managing your tracking models in Django admin, Django Trackman provides the mix-in class
`TrackingModelAdminMixin`.

.. code-block:: python

    from django.contrib import admin
    from trackman.admin import TrackingModelAdminMixin
    from .models import TrackingAction

    class TrackingActionAdmin(TrackingModelAdminMixin, admin.ModelAdmin):
        list_display = [
            "id",
            "actor",
            "team",
            "action",
            "object",
            "target",
            "description",
            "created",
        ]
        search_fields = ["actor", "team"] + TrackingModelAdminMixin.action_log_search_fields
        list_filter = ["team", "action"]

    if settings.TRACKMAN_ENABLED:
      admin.site.register(TrackingAction, TrackingActionAdmin)


Tracking on a separate database
-------------------------------

When you want to isolate tracking data from your main application data for performance,
maintenance or data integrity reasons, you could route tracking database operations to a
separate database.


Django's multiple database feature allows you to use more than one database in your project.
It provides the flexibility to specify which models use which database - that's defined by a
router. Django Trackman uses that feature to isolate you tracking data from your application
data.


You will first need to instruct in your project's settings, the database alias that should be
used.


.. code-block:: python

    TRACKMAN_DATABASE_ALIAS = "tracking"


Then define the database accesses.

.. code-block:: python

    DATABASES = {
        "default": {
            'ENGINE': 'django.db.backends.<app-database>',
            'NAME': <app-database-name>,
            'USER': <-app-database-user>,
            'PASSWORD': <-app-database-password>,
            'HOST': <-app-database-host>,
            'PORT': <-app-database-port>,
        },
    }

    if TRACKMAN_ENABLED:
        DATABASE_ROUTERS = ["trackman.db_routers.TrackmanDatabaseRouter"]
        DATABASES[TRACKMAN_DATABASE_ALIAS] = {
            'ENGINE': 'django.db.backends.<tracking-db>',
            'NAME': <tracking-database-name>,
            'USER': <tracking-database-user>,
            'PASSWORD': <tracking-database-password>,
            'HOST': <tracking-database-host>,
            'PORT': <tracking-database-port>,
        }


If you are using a tool like `dj-database-url` with environnement variables:


.. code-block:: python

    from django.urls import dj_database_url.parse

    DATABASES = {"default": dj_database_url.parse(env("APP_DATABASE_URL"))}

    if TRACKMAN_ENABLED:
        DATABASE_ROUTERS = ["trackman.db_routers.TrackingDatabaseRouter"]
        db_url = env("TRACKING_DATABASE_URL")
        DATABASES[TRACKMAN_DATABASE_ALIAS] = dj_database_url.parse(db_url)


Tracking admin action
---------------------


Django Trackman, allows you to track Django admin actions - the actions that
the admin users are performing.

Setting Up Django Trackman
The main file is trackman/signals.py, and it requires importing in some AppConfig's
ready method.

Let's suppose that you have a backoffice app that you can use to setup signals.


.. code-block:: python

    from django.apps import AppConfig
    import sys

    class BackofficeConfig(AppConfig):
        name = "backoffice"
        verbose_name = "Backoffice"

        def ready(self):
            if "migrate" not in sys.argv:
                import trackman.signals  # noqa


As a consequence, all admin actions will be copied to you tracking table.

## References

- [https://stackoverflow.com/questions/15001444/storing-user-activity-in-django](https://stackoverflow.com/questions/15001444/storing-user-activity-in-django)
- [https://paudelgaurav.github.io/gblog/log_user_activity/](https://paudelgaurav.github.io/gblog/log_user_activity/)
- [https://django.how/resources/django-log-activiies/](https://django.how/resources/django-log-activiies/)
