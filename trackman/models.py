from django.db import models
from django.utils.translation import gettext_lazy as _


class TrackingBaseModel(models.Model):
    """
    The base class that is inherited by models requiring tracking.
    Models that extend this class will be consider as tracking models,
    which matters when it comes to database routing.
    """

    class Meta:
        abstract = True


class TrackingActionModel(TrackingBaseModel):
    """
    This class is intended for models that need to track actions or events
    """

    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)
    action = models.CharField(_("action"), max_length=256, blank=True)
    actor = models.CharField(_("actor"), max_length=256, blank=True)
    object = models.CharField(_("object"), max_length=256, blank=True)
    target = models.CharField(_("target"), max_length=256, blank=True)
    description = models.TextField(_("description"), max_length=256, blank=True)
    data = models.JSONField(_("data"), max_length=256, blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = _("tracking")
        verbose_name_plural = _("tracking")

    def __str__(self):
        return f"{self.created}: {self.actor} {self.action}"
