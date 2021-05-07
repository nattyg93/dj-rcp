"""Schemas for the ratings_central app."""
from typing import Dict, Sequence, Type, Union

from hamcrest import instance_of

from common.test.matchers import IsJsonApiRelationship, IsResourceObject, is_date
from common.test.schemas import JsonApiSchema


class PlayersSchema(JsonApiSchema):
    """Schema for players."""

    resource_name = "players"
    attributes = {
        "rc_id": instance_of(int),
        "rating": instance_of(int),
        "st_dev": instance_of(int),
        "last_played": is_date(),
        "rc_primary_club_id": instance_of(int),
        "name": instance_of(str),
        "address_one": instance_of(str),
        "address_two": instance_of(str),
        "city": instance_of(str),
        "na_state": instance_of(str),
        "world_province": instance_of(str),
        "postal_code": instance_of(str),
        "country": instance_of(str),
        "email": instance_of(str),
        "birth": is_date(),
        "gender": instance_of(str),
        "sport": instance_of(int),
        "usatt_id": instance_of(int),
        "tta_id": instance_of(int),
        "ittf_id": instance_of(int),
        "deceased": instance_of(bool),
    }
    relationships: Dict[str, IsJsonApiRelationship] = {}
    includes: Sequence[Union[Type[IsResourceObject], str]] = []


class ClubsSchema(JsonApiSchema):
    """Schema for clubs."""

    resource_name = "clubs"
    attributes = {
        "rc_id": instance_of(int),
        "name": instance_of(str),
        "nickname": instance_of(str),
        "address_one": instance_of(str),
        "address_two": instance_of(str),
        "city": instance_of(str),
        "na_state": instance_of(str),
        "world_province": instance_of(str),
        "postal_code": instance_of(str),
        "country": instance_of(str),
        "email": instance_of(str),
        "website": instance_of(str),
        "phone": instance_of(str),
        "sport": instance_of(int),
        "status": instance_of(str),
    }
    relationships: Dict[str, IsJsonApiRelationship] = {}
    includes: Sequence[Union[Type[IsResourceObject], str]] = []
