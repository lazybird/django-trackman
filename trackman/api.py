from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response
from trackman.tracking import TrackingHandler


class BaseTrackingAPIMixin:
    """
    A mixin that provides base functionality for tracking API actions and their corresponding details.
    """

    model_alias = None

    def clean_action_details(action_details):
        return action_details

    def handle_track_action(self, action_details, model_alias):
        tracking_handler = TrackingHandler()
        action_log = tracking_handler.track_action(action_details, model_alias)
        return action_log


class TrackingAPIViewMixin(BaseTrackingAPIMixin):
    """
    Define functionality specific to APIView.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for tracking actions. Accepts action details in the request data
        and attempts to track the action using the TrackingHandler and corresponding model alias.
        """

        action_details = request.data.copy()
        action_details = self.clean_action_details(action_details)
        action_log = None
        try:
            action_log = self.handle_track_action(action_details, self.model_alias)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        if not action_log or not action_details:
            return Response(
                {
                    "message": "Tracking action failed",
                    "action_details": action_details,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "message": "Tracking action succeeded",
                "action_log_id": action_log.pk,
                "action_details": action_details,
            },
            status=status.HTTP_201_CREATED,
        )


class TrackingViewSetMixin(TrackingAPIViewMixin):
    """
    Define functionality specific to ViewSet.
    """

    def create(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
