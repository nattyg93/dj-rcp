"""Project wide permission classes."""
from rest_framework import permissions


class DjangoFullModelPermissions(permissions.DjangoModelPermissions):
    """Additionally ensure user has view permission to GET."""

    perms_map = {
        **permissions.DjangoModelPermissions.perms_map,
        "GET": ["%(app_label)s.view_%(model_name)s"],
    }
