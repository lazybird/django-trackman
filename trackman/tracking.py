from trackman import settings as trackman_settings
from trackman import utils as trackman_utils


class TrackingHandler:
    """
    Helper class in charge or writing tracking entries to database.
    """

    def track_action(self, action_details, model_alias=None):
        """
        A generic way to track an action.
        """
        if not trackman_settings.TRACKMAN_ENABLED:
            return None
        if not model_alias:
            model_alias = "default"
        model_class = trackman_utils.get_tracking_model(model_alias)
        action_log = model_class.objects.create(**action_details)
        return action_log


class AdminTrackingHandler(TrackingHandler):
    """
    Helper class that handled Django admin actions.
    """

    def track_admin_action(self, action, user, edited_object, description, data):
        """
        A wrapper around the generic track action.
        """
        action_details = {
            "actor": user,
            "action": action,
            "object": str(edited_object),
            "description": description,
            "data": data,
        }
        self.track_action(action_details)
