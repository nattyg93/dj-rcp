"""User models."""
from typing import List

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager


def get_role_choices():
    """Return the choices for roles."""
    return [(info["name"], info["name"]) for info in settings.AUTH_GROUPS]


class User(AbstractBaseUser, PermissionsMixin):
    """Email and password are required. Other fields are optional."""

    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    objects = UserManager()

    class Meta:
        """Model meta options."""

        verbose_name = _("user")
        verbose_name_plural = _("users")
        swappable = "AUTH_USER_MODEL"

        permissions = [
            ("set_user_roles", "Can set user roles"),
            (
                "set_user_password",
                "Can set user passwords without knowing the current password",
            ),
        ]

    class JSONAPIMeta:
        """JSONAPI meta information."""

        resource_name = "users"

    def get_full_name(self):
        """Return the email (this method is required)."""
        return self.email

    def get_short_name(self):
        """Return the email (this method is required)."""
        return self.email

    @property
    def roles(self):
        """
        Return the groups' names as a list.

        NOTE: Only the groups which are in the choices will be returned.
        """
        valid_roles = {choice[0] for choice in get_role_choices()}
        return [group.name for group in self.groups.all() if group.name in valid_roles]
