Django Trackman
===============


Django Trackman helps with tracking and logging.


Features
--------

- Customizable models: You'll have base models and an admin class mixins
  that you can extend to define your own tracking models.

- Separate database: You can decide to use a separate database for your tracking data, as it could
  grow fast. A database router will help you implement the Django multiple database feature.

- Loose coupling: The tracking table is not related to you application table with foreign keys.
  This ensures that your tracking data is kept independent of your application data.

- Admin action tracking: You can enable tracking of Django admin actions.

- API Endpoint: You can define django-rest-framework views to create API endpoints. This can be 
  used to track actions made through API calls.


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


Action Tracking Models
----------------------

Django Trackman can be used to create custom tracking models.
Here's an example of a model class that extends Django Trackman's `TrackingActionModel``:


.. code-block:: python

    from trackman.models import TrackingActionModel
    from django.db import models

    class TrackingAction(TrackingActionModel):
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


Base Tracking Models
--------------------

If your models are not action oriented, you can always extend the `TrackingBaseModel`
that's an empty abstract model that only serves as a way to let Trackman know that
your model should be consider as a tracking model and thus should be taken into account
when during database routing.


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


API End-point
-------------

Django Trackman provides a mixin you can use with Django Rest Framework's ViewSet to create an API end-point
for your application to track actions. This could be useful for tracking front-end actions.

Here's how you can use TrackingViewSetMixin in a Django REST ViewSet for action tracking:

.. code-block:: python

    from rest_framework import viewsets
    from trackman.api import TrackingViewSetMixin

    class ActionTrackingViewSet(TrackingViewSetMixin, viewsets.ViewSet):
        model_alias = "default"

        def clean_action_details(self, action_details):
            # Do some clean-up here...
            cleaned_data = action_details.copy()
            return cleaned_data



The `model_alias` points out which Django Trackman model alias to be used for saving the tracking data.

You'll need to add this new ViewSet ActionTrackingViewSet to your url configuration to have it active.

