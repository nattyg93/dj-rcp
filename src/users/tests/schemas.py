"""Schemas for users app."""
from typing import Dict, Sequence, Type, Union

from django.conf import settings
from hamcrest import any_of, empty, instance_of, only_contains

from common.test.matchers import IsJsonApiRelationship, IsResourceObject, is_to_one
from common.test.schemas import JsonApiSchema


class UsersSchema(JsonApiSchema):
    """Schema for users."""

    resource_name = "users"
    attributes = {
        "email": instance_of(str),
        "roles": any_of(
            empty(), only_contains(*[group["name"] for group in settings.AUTH_GROUPS])
        ),
    }
    relationships: Dict[str, IsJsonApiRelationship] = {}
    includes: Sequence[Union[Type[IsResourceObject], str]] = []


class SessionsSchema(JsonApiSchema):
    """Schema for sessions."""

    resource_name = "sessions"
    attributes = {"token": instance_of(str)}
    relationships = {"user": is_to_one(resource_name="users")}
    includes: Sequence[Union[Type[IsResourceObject], str]] = []
