from django.contrib import admin

MODEL_ADMIN_SEARCH_FIELDS = [
    "action",
    "object",
    "target",
    "description",
    "data",
]


class ReadOnlyAdminMixin:
    """
    Model admin class that prevents modifications through the admin.
    """

    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TrackingModelAdminMixin(ReadOnlyAdminMixin):
    """
    Mixin admin class for models that extends TrackingBaseModel.
    """

    list_display = [
        "id",
        "user",
        "team",
        "action",
        "object",
        "target",
        "description",
        "created",
    ]
    search_fields = MODEL_ADMIN_SEARCH_FIELDS
