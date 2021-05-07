"""Serializers for users app."""
# pylint: disable=abstract-method
from collections import Counter
from uuid import uuid4

import dj_rest_auth.serializers
import django.core.exceptions
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from rest_framework_json_api import serializers

from users.models import User, get_role_choices

RESET_TEMPLATES = {
    "email_template_name": "registration/password_reset_email.txt",
    "html_email_template_name": "registration/password_reset_email.html",
}


class _UuidPk:
    def __init__(self):
        self.pk = str(uuid4())  # pylint: disable=invalid-name


class SessionSerializer(serializers.Serializer):
    """Session serializer."""

    user = serializers.ResourceRelatedField(model=User, read_only=True)

    class JSONAPIMeta:
        """JSONAPI meta information."""

        resource_name = "sessions"


class TokenSerializer(
    serializers.IncludedResourcesValidationMixin,
    serializers.SparseFieldsetsMixin,
    dj_rest_auth.serializers.TokenSerializer,
):
    """Set the pk of the instance to be the user's pk."""

    token = serializers.CharField(read_only=True, source="_backup_key")
    user = serializers.ResourceRelatedField(read_only=True)

    class Meta(dj_rest_auth.serializers.TokenSerializer.Meta):
        """Serializer meta information."""

        fields = ["token", "user"]

    class JSONAPIMeta:
        """JSONAPI meta information."""

        resource_name = "sessions"

    def __init__(self, *args, **kwargs):
        """Set the pk of the instance to be the user's pk."""
        super().__init__(*args, **kwargs)
        if getattr(self, "instance", None):
            self.instance._backup_key = self.instance.pk
            self.instance.pk = self.context["request"].user.pk


class LoginSerializer(
    serializers.IncludedResourcesValidationMixin,
    serializers.SparseFieldsetsMixin,
    dj_rest_auth.serializers.LoginSerializer,
):
    """Login serializer that removes case."""

    class JSONAPIMeta:
        """JSONAPI meta information."""

        resource_name = "sessions"

    def validate_email(self, value):  # pylint: disable=no-self-use
        """Login serializer that removes case."""
        return value.casefold()


class PasswordResetSerializer(  # pylint: disable=abstract-method
    serializers.IncludedResourcesValidationMixin,
    serializers.SparseFieldsetsMixin,
    dj_rest_auth.serializers.PasswordResetSerializer,
):
    """Password reset serializer that removes case."""

    def __init__(self, *args, **kwargs):
        """Get welcome from the kwargs."""
        self.welcome = kwargs.pop("welcome", False)
        super().__init__(*args, **kwargs)

    class JSONAPIMeta:
        """JSONAPI meta information."""

        resource_name = "password-resets"

    def get_email_context(self):
        """Casefold the email address before encoding it."""
        email = self.data["email"].casefold().encode("utf-8")
        email_encoded = urlsafe_base64_encode(email)
        return {"email_encoded": email_encoded, "project_name": settings.PROJECT_NAME}

    def get_email_options(self):
        """Update email options."""
        opts = {
            **super().get_email_options(),
            **RESET_TEMPLATES,
            "extra_email_context": self.get_email_context(),
        }
        if self.welcome:
            opts.update(
                {
                    "subject_template_name": "users/emails/welcome_email_subject.txt",
                    "email_template_name": "users/emails/welcome_email.txt",
                    "html_email_template_name": "users/emails/welcome_email.html",
                }
            )
        return opts

    def validate_email(self, value):
        """Casefold the email address before validation."""
        return super().validate_email(value.casefold())

    def save(self):
        """Add an instance with a pk for the json api renderer."""
        super().save()
        if getattr(self, "instance", None) is None:
            self.instance = _UuidPk()


class PasswordResetConfirmSerializer(
    serializers.IncludedResourcesValidationMixin,
    serializers.SparseFieldsetsMixin,
    dj_rest_auth.serializers.PasswordResetConfirmSerializer,
):
    """Make the fields write only."""

    new_password1 = serializers.CharField(write_only=True, max_length=128)
    new_password2 = serializers.CharField(write_only=True, max_length=128)
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class JSONAPIMeta:
        """JSONAPI meta information."""

        resource_name = "password-reset-confirmations"

    def save(self):
        """Add an instance with a pk for the json api renderer."""
        to_return = super().save()
        if getattr(self, "instance", None) is None:
            self.instance = _UuidPk()
        return to_return


class UserSerializer(serializers.ModelSerializer):
    """Users serializer."""

    current_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    roles = serializers.ListField(
        child=serializers.ChoiceField(choices=get_role_choices()),
        required=False,
        error_messages={"not_a_list": "Expected a list of strings."},
    )

    class Meta:
        """Serializer meta information."""

        model = User
        fields = ["email", "password", "current_password", "roles"]

    def create(self, validated_data):
        """Create the user with the given email and password."""
        password = validated_data.pop("password", None)
        instance = super().create(validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
        else:
            self._send_welcome_email(instance)
        return instance

    def _send_welcome_email(self, user) -> None:
        """Send welcome email to new user using PasswordResetSerializer."""
        serializer = PasswordResetSerializer(
            welcome=True, context=self.context, data={"email": user.email}
        )
        serializer.is_valid()
        serializer.save()

    def update(self, instance, validated_data):
        """Set the password on the instance."""
        if "password" in validated_data:
            instance.set_password(validated_data.pop("password"))
        return super().update(instance, validated_data)

    def validate_email(self, value):  # pylint: disable=no-self-use
        """Casefold the email address before validation."""
        return value.casefold()

    def validate_roles(self, roles):
        """Check user permissions."""
        # We use a Counter since the order of the roles does not matter
        if Counter(getattr(self.instance, "roles", [])) != Counter(roles):
            if not self.context["request"].user.has_perm("users.set_user_roles"):
                raise serializers.ValidationError(
                    "You do not have permission to set this field."
                )
        return roles

    def validate(self, attrs):
        """Validate data."""
        attrs = super().validate(attrs)
        if "password" in attrs and attrs["password"] == "":
            # treat a blank string as the password not having been set
            attrs.pop("password")
        password_set = "password" in attrs
        # updating
        if self.instance is not None:
            # cannot update email address
            attrs.pop("email", None)
            # when changing password validate current_password
            if password_set:
                self._validate_current_password(attrs.get("current_password"))
        # validate the password if it is included
        if password_set:
            self._validate_password(attrs["password"])
        self._validate_roles(attrs)
        return attrs

    def _validate_current_password(self, current_password):
        user = self.context["request"].user
        if current_password is not None:
            if not self.instance.check_password(current_password):
                msg = _("Your current password is incorrect.")
                raise serializers.ValidationError({"current_password": msg})
        elif not user.has_perm("users.set_user_password"):
            msg = _("This field is required when changing your password.")
            raise serializers.ValidationError({"current_password": msg})

    def _validate_password(self, password):  # pylint: disable=no-self-use
        try:
            validate_password(password)
        except django.core.exceptions.ValidationError as error:
            raise serializers.ValidationError({"password": error.messages})

    def _validate_roles(self, attrs):  # pylint: disable=no-self-use
        """Get groups from roles."""
        roles = attrs.pop("roles", None)
        if roles is None:
            return
        if len(roles) != len(set(roles)):
            raise serializers.ValidationError(
                {"roles": "This field cannot contain duplicate entries."}
            )
        groups = Group.objects.filter(name__in=roles)
        attrs["groups"] = groups
