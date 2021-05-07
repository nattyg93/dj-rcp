"""Tests for clubs endpoint."""
from __future__ import annotations

from typing import Type

from common.test import JsonApiTestCase, mixins
from common.test.schemas import JsonApiSchema
from ratings_central.tests import factories, schemas


class EndpointConfig(
    mixins.FactoryDataMixin, mixins.DefaultDataMixin, mixins.PermissionCodeMixin
):
    """Define endpoint-wide configuration."""

    factory = factories.ClubFactory
    permission_model_name = "club"
    app_label = "ratings_central"
    schema: Type[JsonApiSchema] = schemas.ClubsSchema

    def get_default_post_values(self):
        """Return default values required for a successful post."""
        return {}

    def get_default_patch_values(self):
        """Return default values required for a successful patch."""
        return {}


class AnonTestCase(EndpointConfig, mixins.readonly.AnonTestCaseMixin, JsonApiTestCase):
    """Test validation for anon users."""


class UserTestCase(
    EndpointConfig,
    mixins.readonly.TrueReadOnlyMixin,
    mixins.readonly.UserTestCaseMixin,
    JsonApiTestCase,
):
    """Test validation for authed users."""


class PrivilegedTestCase(
    EndpointConfig,
    mixins.readonly.TrueReadOnlyMixin,
    mixins.readonly.PrivilegedTestCaseMixin,
    JsonApiTestCase,
):
    """Test validation on users endpoint."""
