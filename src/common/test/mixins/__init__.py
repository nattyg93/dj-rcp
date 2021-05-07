"""Test mixins."""
from typing import Any, Dict, Iterable, Type

import factory
from django.contrib.auth.models import Permission
from django.db.models import Model

from . import failure, readonly, success


class PermissionCodeMixin:
    """Add shortcut for getting permissions for endpoints."""

    permission_model_name: str
    app_label: str

    permission_mapping = {
        "create": "{app_label}.add_{permission_model_name}",
        "retrieve": "{app_label}.view_{permission_model_name}",
        "update": "{app_label}.change_{permission_model_name}",
        "delete": "{app_label}.delete_{permission_model_name}",
    }

    def __init__(self, *args, **kwargs):
        """Raise error if permission_model_name is set."""
        super().__init__(*args, **kwargs)
        assert self.permission_model_name is not None, (
            "`permission_model_name` must be specified "
            "in subclasses of PermissionCodeMixin"
        )

        assert (
            self.app_label is not None
        ), "`app_label` must be specified in subclasses of PermissionCodeMixin"

    def give_perms(self, *actions, **kwargs):
        """Give the currently authed user permissions for the given actions."""
        if self.current_user is None:
            raise ValueError("There is no currently authenticated user.")
        perms = self.perms(*actions, **kwargs)
        for perm in perms:
            app_label, codename = perm.split(".")
            permission = Permission.objects.filter(
                content_type__app_label=app_label, codename=codename
            ).first()
            if permission is None:
                raise ValueError(
                    f"The permission identified by `{perm}`"
                    " does not exist in the database."
                )
            self.current_user.user_permissions.add(permission)

    def perms(self, *actions, **kwargs):
        """Return the permission for the given action."""
        kwargs.setdefault("permission_model_name", self.permission_model_name)
        kwargs.setdefault("app_label", self.app_label)
        permission_codes = []
        for action in actions:
            try:
                permission_codes.append(
                    self.permission_mapping[action].format(**kwargs)
                )
            except KeyError as error:
                raise ValueError(
                    f"The given action `{action}` is not specified in the permission_mapping"
                ) from error
        return permission_codes


class DefaultDataMixin:
    """Provide methods to easily get default data for POSTing and PATCHing."""

    def get_default_post_values(self) -> Dict[str, Any]:
        """Return the dictionary of POST defaults."""
        raise NotImplementedError

    def get_post_data(self, exclude: Iterable[str] = tuple(), **kwargs):
        """Return post data which will succeed in creating an instance."""
        merged = {**self.get_default_post_values(), **kwargs}
        values = {
            key: val() if callable(val) else val
            for key, val in merged.items()
            if key not in exclude
        }
        return {"data": self.schema.get_data(**values)}  # type: ignore

    def get_default_patch_values(self) -> Dict[str, Any]:
        """Return the dictionary of PATCH defaults."""
        raise NotImplementedError

    def get_patch_data(
        self, exclude: Iterable[str] = tuple(), **kwargs
    ) -> Dict[str, Any]:
        """Return patch data which will succeed in updating an instance."""
        merged = {**self.get_default_patch_values(), **kwargs}
        values = {
            key: val() if callable(val) else val
            for key, val in merged.items()
            if key not in exclude
        }
        return {"data": self.schema.get_data(**values)}  # type: ignore


class FactoryDataMixin:
    """Automatically setup default data from mixins."""

    batch_size = 3
    factory: Type[factory.Factory]
    factory_kwargs: Dict[str, Any] = {}
    instance: Model
    instances: Iterable[Model]

    @classmethod
    def setUpClass(cls):  # pylint: disable=invalid-name
        """Set up the required attributes for the tests."""
        super().setUpClass()
        assert cls.batch_size >= 0, "batch_size must be greater than 0"
        if cls.batch_size <= 0:
            # let the subclass handle creation
            return
        cls.instances = cls.factory.create_batch(
            **cls.factory_kwargs, size=cls.batch_size
        )
        cls.instance = cls.instances[0]
