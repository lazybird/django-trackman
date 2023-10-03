import json

from django.contrib.admin.models import LogEntry
from django.core import serializers
from django.db.models.signals import post_save
from django.dispatch import receiver

from trackman import settings as trackman_settings
from trackman import utils as trackman_utils

AdminTrackingHandler = trackman_utils.get_admin_tracking_class()
admin_tracker = AdminTrackingHandler()


@receiver(post_save, sender=LogEntry)
def track_admin_action(sender, instance, **kwargs):
    """
    Track a log entry after for admin actions
    """
    action_labels = trackman_settings.ADMIN_ACTION_LABELS
    action = ""
    if instance.is_change():
        action = action_labels["change"]
    if instance.is_deletion():
        action = action_labels["deletion"]
    if instance.is_addition():
        action = action_labels["addition"]
    edited_object = instance.get_edited_object()
    edited_object_json = serializers.serialize("json", [edited_object])
    edited_object_data = json.loads(edited_object_json)
    admin_tracker.track_admin_action(
        action=action,
        user=instance.user,
        edited_object=edited_object,
        description=instance.change_message,
        data=edited_object_data,
    )
